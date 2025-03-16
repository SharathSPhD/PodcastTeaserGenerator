"""
Audio analysis functions for podcast teaser generation
"""

import numpy as np
import librosa
import scipy.signal as signal
from . import config
from .defaults import DEFAULT_CONFIG

logger = config.logger

def load_audio(file_path, sr=22050):
    """Load audio file using librosa"""
    logger.info(f"Loading audio file: {file_path}")
    try:
        y, sr = librosa.load(file_path, sr=sr)
        logger.info(f"Successfully loaded audio: {len(y)/sr:.2f} seconds @ {sr}Hz")
        return y, sr
    except Exception as e:
        logger.error(f"Error loading audio file: {e}")
        raise

def get_transcript_score_array(transcript_segments, num_frames, sr, hop_length):
    """
    Convert transcript segment scores to a frame-aligned array
    
    Args:
        transcript_segments: List of segments with timestamps and importance scores
        num_frames: Number of frames in audio analysis
        sr: Sample rate
        hop_length: Hop length used in analysis
        
    Returns:
        numpy.ndarray: Array of transcript scores aligned with audio frames
    """
    transcript_score = np.zeros(num_frames)
    
    if not transcript_segments:
        return transcript_score
        
    for segment in transcript_segments:
        # Convert segment times to frame indices
        start_frame = int(segment['start'] * sr / hop_length)
        end_frame = int(segment['end'] * sr / hop_length)
        
        # Clip to valid range
        start_frame = max(0, min(start_frame, num_frames-1))
        end_frame = max(0, min(end_frame, num_frames-1))
        
        # Set score for segment duration
        if end_frame > start_frame:
            transcript_score[start_frame:end_frame] = segment['importance']
    
    return transcript_score

def analyze_audio(y, sr, config_dict):
    """Analyze audio to find interesting segments"""
    logger.info("Starting audio analysis...")
    
    # Get duration
    duration = librosa.get_duration(y=y, sr=sr)
    logger.info(f"Audio duration: {duration:.2f} seconds")
    
    # Set processing parameters
    hop_length = int(sr * 0.02)  # 20ms hop
    frame_length = int(sr * 0.04)  # 40ms frames
    
    # 1. Calculate RMS energy (volume/excitement)
    logger.info("Calculating RMS energy...")
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_norm = (rms - np.mean(rms)) / (np.std(rms) + 1e-6)
    
    # 2. Spectral contrast (dramatic moments, tonal variation)
    logger.info("Calculating spectral contrast...")
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=hop_length)
    contrast_mean = np.mean(contrast, axis=0)
    contrast_norm = (contrast_mean - np.mean(contrast_mean)) / (np.std(contrast_mean) + 1e-6)
    
    # 3. Speech tempo analysis
    logger.info("Analyzing speech tempo...")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    window_size = 20  # ~0.4 seconds
    tempo_changes = np.zeros_like(onset_env)
    padded_onset = np.pad(onset_env, (window_size//2, window_size//2), mode='edge')
    for i in range(len(onset_env)):
        tempo_changes[i] = np.std(padded_onset[i:i+window_size])
    tempo_norm = (tempo_changes - np.mean(tempo_changes)) / (np.std(tempo_changes) + 1e-6)
    
    # 4. Silence detection
    logger.info("Detecting silence regions...")
    db_threshold = config_dict['silence_threshold']
    db = librosa.amplitude_to_db(rms)
    silence_mask = db < db_threshold
    
    # Get audio feature weights
    audio_features = config_dict.get('analysis_weights', {}).get('audio_features', 
                                   DEFAULT_CONFIG['analysis_weights']['audio_features'])
    
    # Compute audio-based score
    audio_score = (
        audio_features['energy_weight'] * rms_norm +
        audio_features['spectral_weight'] * contrast_norm +
        audio_features['tempo_weight'] * tempo_norm
    )
    
    # Smooth the audio score
    audio_score = signal.savgol_filter(audio_score, 11, 3)
    
    # Convert frames to timestamps
    timestamps = librosa.frames_to_time(np.arange(len(audio_score)), sr=sr, hop_length=hop_length)
    
    analysis_results = {
        'audio_score': audio_score,
        'timestamps': timestamps,
        'duration': duration,
        'rms_norm': rms_norm,
        'contrast_norm': contrast_norm,
        'tempo_norm': tempo_norm,
        'silence_mask': silence_mask,
        'hop_length': hop_length,
        'sr': sr
    }
    
    logger.info("Audio analysis complete")
    return analysis_results

def find_highlight_segments(analysis_results, config_dict):
    """Find the most interesting segments for the teaser"""
    logger.info("Finding highlight segments...")
    
    # Get basic parameters
    timestamps = analysis_results['timestamps']
    silence_mask = analysis_results['silence_mask']
    sr = analysis_results['sr']
    hop_length = analysis_results['hop_length']
    
    # Get analysis weights
    weights = config_dict.get('analysis_weights', DEFAULT_CONFIG['analysis_weights'])
    audio_weight = weights.get('audio_dynamics', 0.4)
    transcript_weight = weights.get('transcript_importance', 0.6)
    
    # Start with audio score
    audio_score = analysis_results['audio_score']
    
    # Get transcript score if available
    transcript_score = np.zeros_like(audio_score)
    if 'transcript_segments' in analysis_results:
        transcript_score = get_transcript_score_array(
            analysis_results['transcript_segments'],
            len(audio_score),
            sr,
            hop_length
        )
        logger.info("Incorporated transcript scores into analysis")
    else:
        logger.info("No transcript scores available, using audio-only analysis")
        # If no transcript, use only audio score
        audio_weight = 1.0
        transcript_weight = 0.0
    
    # Combine scores
    interest_score = (audio_weight * audio_score + transcript_weight * transcript_score)
    
    # Penalize intro/outro sections if enabled
    if config_dict.get('exclude_intro_outro', True):
        penalty = -10.0  # Large negative score to avoid selection
        intro_frames = int(config_dict.get('intro_duration', 30) * sr / hop_length)
        outro_frames = int(config_dict.get('outro_duration', 30) * sr / hop_length)
        
        if intro_frames > 0 and intro_frames < len(interest_score):
            interest_score[:intro_frames] = penalty
            logger.info(f"Excluded intro: first {config_dict.get('intro_duration', 30)} seconds")
        
        if outro_frames > 0 and outro_frames < len(interest_score):
            interest_score[-outro_frames:] = penalty
            logger.info(f"Excluded outro: last {config_dict.get('outro_duration', 30)} seconds")
    
    # Smooth the combined score
    interest_score = signal.savgol_filter(interest_score, 11, 3)
    
    # Find peaks (most interesting moments)
    min_dist = int(config_dict['segment_min_duration'] * sr / hop_length / 2)
    peaks, _ = signal.find_peaks(interest_score, distance=min_dist)
    
    # Sort peaks by interest score
    sorted_peaks = sorted(peaks, key=lambda x: interest_score[x], reverse=True)
    
    # Select top peaks
    num_peaks = min(len(sorted_peaks), config_dict['num_segments']*2)
    candidate_peaks = sorted_peaks[:num_peaks]
    
    # For each peak, find optimal segment boundaries
    segments = []
    min_segment_frames = int(config_dict['segment_min_duration'] * sr / hop_length)
    max_segment_frames = int(config_dict['segment_max_duration'] * sr / hop_length)
    
    for peak in candidate_peaks:
        # Search backward for start point
        start_idx = max(0, peak - max_segment_frames)
        for i in range(peak-1, start_idx, -1):
            if silence_mask[i]:
                start_idx = i
                break
                
        # Search forward for end point
        end_idx = min(len(interest_score)-1, peak + max_segment_frames)
        for i in range(peak+1, end_idx):
            if silence_mask[i]:
                end_idx = i
                break
        
        # Ensure minimum segment length
        if end_idx - start_idx < min_segment_frames:
            continue
            
        # Ensure maximum segment length
        if end_idx - start_idx > max_segment_frames:
            half_length = max_segment_frames // 2
            start_idx = max(0, peak - half_length)
            end_idx = min(len(interest_score)-1, peak + half_length)
        
        # Convert frame indices to timestamps
        start_time = timestamps[start_idx]
        end_time = timestamps[end_idx]
        
        segments.append((start_time, end_time))
    
    # Sort segments by timestamp
    segments.sort(key=lambda x: x[0])
    
    # Remove overlapping segments
    filtered_segments = []
    for segment in segments:
        overlap = False
        for filtered in filtered_segments:
            if (segment[0] < filtered[1] and segment[1] > filtered[0]):
                overlap = True
                break
        
        if not overlap:
            filtered_segments.append(segment)
    
    # Take the top N segments based on config
    if len(filtered_segments) > config_dict['num_segments']:
        segment_scores = []
        for start, end in filtered_segments:
            start_idx = np.argmin(np.abs(timestamps - start))
            end_idx = np.argmin(np.abs(timestamps - end))
            avg_score = np.mean(interest_score[start_idx:end_idx])
            segment_scores.append(avg_score)
            
        top_indices = np.argsort(segment_scores)[-config_dict['num_segments']:]
        filtered_segments = [filtered_segments[i] for i in sorted(top_indices)]
    
    # Sort final segments by time
    filtered_segments.sort(key=lambda x: x[0])
    
    # Log analysis weights used
    logger.info(f"Analysis weights - Audio: {audio_weight:.2f}, Transcript: {transcript_weight:.2f}")
    logger.info(f"Found {len(filtered_segments)} highlight segments")
    
    return filtered_segments
