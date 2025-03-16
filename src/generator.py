"""
Teaser extraction and generation functionality
"""

import os
import json
from datetime import datetime
from pydub import AudioSegment
from pydub.effects import normalize
from . import config
from . import analysis
from . import visualization

logger = config.logger

def extract_teaser(input_file, segments, output_path, config_dict):
    """
    Extract the segments from the audio file and create the teaser
    
    Args:
        input_file: Path to input audio file
        segments: List of (start_time, end_time) tuples
        output_path: Path to save the teaser
        config_dict: Configuration dictionary
        
    Returns:
        str: Path to the created teaser file
    """
    logger.info(f"Extracting teaser from {len(segments)} segments...")
    
    # Load the audio file with pydub
    try:
        audio = AudioSegment.from_file(input_file)
        logger.info(f"Loaded audio with pydub: {len(audio)/1000:.2f} seconds")
    except Exception as e:
        logger.error(f"Error loading audio with pydub: {e}")
        raise
    
    # Extract segments
    audio_segments = []
    for i, (start, end) in enumerate(segments):
        start_ms = int(start * 1000)
        end_ms = int(end * 1000)
        segment = audio[start_ms:end_ms]
        logger.info(f"Extracted segment {i+1}: {start:.2f}s - {end:.2f}s ({len(segment)/1000:.2f}s)")
        audio_segments.append(segment)
    
    # Combine segments with crossfade
    crossfade = config_dict['crossfade_duration']
    if len(audio_segments) > 0:
        teaser = audio_segments[0]
        for segment in audio_segments[1:]:
            if len(teaser) > crossfade and len(segment) > crossfade:
                teaser = teaser.append(segment, crossfade=crossfade)
            else:
                # If segments are too short for crossfade, just append
                teaser = teaser + segment
    else:
        logger.error("No segments found, cannot create teaser")
        return None
    
    # Normalize audio levels if requested
    if config_dict['normalize_audio']:
        logger.info("Normalizing audio levels...")
        teaser = normalize(teaser)
    
    # Make sure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Export the teaser
    output_format = config_dict['output_format']
    logger.info(f"Exporting teaser to {output_path} in {output_format} format...")
    teaser.export(output_path, format=output_format)
    
    logger.info(f"Teaser created successfully: {len(teaser)/1000:.2f} seconds")
    return output_path

def process_podcast(input_file, output_dir, config_dict):
    """
    Process a single podcast file and create a teaser
    
    Args:
        input_file: Path to podcast file
        output_dir: Directory to save output files
        config_dict: Configuration dictionary
        
    Returns:
        str: Path to created teaser file
    """
    logger.info(f"Processing podcast: {input_file}")
    
    # Create output filename
    basename = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{basename}_teaser_{timestamp}.{config_dict['output_format']}")
    
    # Step 1: Load and analyze audio
    y, sr = analysis.load_audio(input_file)
    
    # Step 2: Get transcription if enabled
    from . import transcription
    transcript_result = transcription.transcribe_audio(input_file, config_dict)
    
    # Step 3: Process transcript and get segment importance
    transcript_segments = []
    if transcript_result:
        for segment in transcript_result['segments']:
            importance = transcription.get_segment_importance(segment, config_dict)
            transcript_segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'],
                'importance': importance
            })
    
    # Step 4: Analyze audio with transcript information
    analysis_results = analysis.analyze_audio(y, sr, config_dict)
    if transcript_segments:
        analysis_results['transcript_segments'] = transcript_segments
    
    # Step 2: Find highlight segments
    segments = analysis.find_highlight_segments(analysis_results, config_dict)
    
    # Step 3: Create visualization if requested
    if config_dict['visualize']:
        viz_prefix = os.path.join(output_dir, f"{basename}_teaser_{timestamp}")
        visualization.visualize_analysis(analysis_results, segments, viz_prefix)
    
    # Step 4: Extract and create teaser
    teaser_path = extract_teaser(input_file, segments, output_file, config_dict)
    
    # Save analysis and configuration metadata
    metadata = {
        'input_file': input_file,
        'output_file': output_file,
        'timestamp': timestamp,
        'config': config_dict,
        'segments': segments,
        'duration': analysis_results['duration'],
        'teaser_duration': sum(end-start for start, end in segments)
    }
    
    metadata_path = os.path.join(output_dir, f"{basename}_teaser_{timestamp}_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return teaser_path

def create_summary_teaser(teaser_files, output_path, config_dict):
    """
    Create a summary teaser by combining segments from multiple individual teasers
    
    Args:
        teaser_files: List of paths to individual teaser files
        output_path: Path to save the summary teaser
        config_dict: Configuration dictionary
        
    Returns:
        str: Path to the created summary teaser file
    """
    if not teaser_files:
        logger.error("No teaser files provided for summary creation")
        return None
        
    logger.info(f"Creating summary teaser from {len(teaser_files)} individual teasers")
    
    # Load metadata files to get segment information
    all_segments = []
    track_info = []
    
    for teaser_path in teaser_files:
        # Find corresponding metadata file
        base_path = os.path.splitext(teaser_path)[0]
        metadata_path = f"{base_path}_metadata.json"
        
        if not os.path.exists(metadata_path):
            logger.warning(f"Metadata not found for {teaser_path}, skipping")
            continue
            
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                
            # Get original input file and segments
            input_file = metadata['input_file']
            segments = metadata['segments']
            
            # Sort segments by interest score if available, otherwise use as is
            if isinstance(segments, list) and len(segments) > 0:
                # Select top N segments based on config
                segments_to_use = segments[:config_dict['summary_segments_per_track']]
                
                # Store segments with track info
                for segment in segments_to_use:
                    all_segments.append({
                        'input_file': input_file,
                        'start': segment[0],
                        'end': segment[1],
                        'duration': segment[1] - segment[0]
                    })
                    
                track_info.append({
                    'file': input_file,
                    'basename': os.path.basename(input_file)
                })
                
        except Exception as e:
            logger.error(f"Error processing metadata for {teaser_path}: {e}")
    
    if not all_segments:
        logger.error("No valid segments found in any teaser metadata")
        return None
    
    # Sort segments by interest score or duration
    all_segments.sort(key=lambda x: x['duration'], reverse=True)
    
    # Calculate total target duration and adjust if needed
    target_duration = config_dict['summary_teaser_duration']
    segments_to_include = []
    current_duration = 0
    
    # Add segments until we reach target duration
    for segment in all_segments:
        if current_duration + segment['duration'] <= target_duration:
            segments_to_include.append(segment)
            current_duration += segment['duration']
        else:
            # If we're close enough to target, stop adding
            if current_duration >= target_duration * 0.8:
                break
                
            # Otherwise, trim this segment to fit
            remaining_duration = target_duration - current_duration
            if remaining_duration >= 3:  # Only add if at least 3 seconds
                segment['end'] = segment['start'] + remaining_duration
                segment['duration'] = remaining_duration
                segments_to_include.append(segment)
                current_duration += remaining_duration
                break
    
    if not segments_to_include:
        logger.error("Could not create summary teaser: no segments selected")
        return None
    
    logger.info(f"Selected {len(segments_to_include)} segments for summary teaser, total duration: {current_duration:.2f}s")
    
    # Extract and combine segments
    audio_segments = []
    for i, segment in enumerate(segments_to_include):
        try:
            # Load the audio file with pydub
            audio = AudioSegment.from_file(segment['input_file'])
            
            # Extract segment
            start_ms = int(segment['start'] * 1000)
            end_ms = int(segment['end'] * 1000)
            segment_audio = audio[start_ms:end_ms]
            
            logger.info(f"Extracted segment {i+1} from {os.path.basename(segment['input_file'])}: "
                       f"{segment['start']:.2f}s - {segment['end']:.2f}s ({segment['duration']:.2f}s)")
                       
            audio_segments.append(segment_audio)
        except Exception as e:
            logger.error(f"Error extracting segment from {segment['input_file']}: {e}")
    
    if not audio_segments:
        logger.error("Failed to extract any audio segments for summary teaser")
        return None
    
    # Combine segments with crossfade
    crossfade = config_dict['crossfade_duration']
    if len(audio_segments) > 0:
        summary_teaser = audio_segments[0]
        for segment in audio_segments[1:]:
            if len(summary_teaser) > crossfade and len(segment) > crossfade:
                summary_teaser = summary_teaser.append(segment, crossfade=crossfade)
            else:
                summary_teaser = summary_teaser + segment
    else:
        logger.error("No segments to combine for summary teaser")
        return None
    
    # Normalize audio levels if requested
    if config_dict['normalize_audio']:
        logger.info("Normalizing summary teaser audio levels...")
        summary_teaser = normalize(summary_teaser)
    
    # Export the summary teaser
    output_format = config_dict['output_format']
    logger.info(f"Exporting summary teaser to {output_path} in {output_format} format...")
    summary_teaser.export(output_path, format=output_format)
    
    # Save summary metadata
    summary_metadata = {
        'created_at': datetime.now().isoformat(),
        'duration': len(summary_teaser) / 1000,
        'source_tracks': track_info,
        'segments': [{'file': s['input_file'], 'start': s['start'], 'end': s['end']} for s in segments_to_include],
        'config': config_dict
    }
    
    metadata_path = os.path.splitext(output_path)[0] + "_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(summary_metadata, f, indent=2)
    
    logger.info(f"Summary teaser created successfully: {len(summary_teaser)/1000:.2f} seconds")
    return output_path
