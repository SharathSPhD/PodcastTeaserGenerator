"""
Transcription module using Whisper for offline speech-to-text
"""

import os
import json
import hashlib
from datetime import datetime
from . import config
from .defaults import DEFAULT_CONFIG

logger = config.logger

def get_default_transcription_config():
    """Get default transcription settings"""
    return DEFAULT_CONFIG['transcription']

def ensure_transcription_config(config_dict):
    """Ensure config has transcription settings"""
    if 'transcription' not in config_dict:
        config_dict['transcription'] = get_default_transcription_config()
    return config_dict

def get_cache_path(audio_path, config_dict):
    """Get cache path for transcript based on audio file hash"""
    config_dict = ensure_transcription_config(config_dict)
    cache_dir = config_dict['transcription'].get('cache_dir', 'transcripts')
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    # Get audio file hash for unique identification
    with open(audio_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    
    basename = os.path.splitext(os.path.basename(audio_path))[0]
    cache_name = f"{basename}_{file_hash}_transcript.json"
    
    return os.path.join(cache_dir, cache_name)

def load_cached_transcript(cache_path):
    """Load transcript from cache if it exists"""
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                logger.info(f"Loaded cached transcript from {cache_path}")
                return data
        except Exception as e:
            logger.warning(f"Failed to load cached transcript: {e}")
    return None

def save_transcript(transcript, cache_path):
    """Save transcript to cache"""
    try:
        transcript_data = {
            'transcript': transcript,
            'timestamp': datetime.now().isoformat(),
            'model': DEFAULT_CONFIG['transcription']['model']
        }
        
        with open(cache_path, 'w') as f:
            json.dump(transcript_data, f, indent=2)
        logger.info(f"Saved transcript to {cache_path}")
    except Exception as e:
        logger.error(f"Failed to save transcript: {e}")

def init_whisper():
    """Initialize Whisper model with error handling"""
    try:
        import whisper
        logger.info("Attempting to load Whisper model...")
        model = whisper.load_model("base", download_root="models")
        logger.info("Whisper model loaded successfully")
        return model
    except ImportError:
        logger.error("Failed to import Whisper. Please install it using: pip install -U openai-whisper")
        return None
    except Exception as e:
        logger.error(f"Error loading Whisper model: {e}")
        return None

def transcribe_audio(audio_path, config_dict):
    """Transcribe audio using Whisper with caching"""
    config_dict = ensure_transcription_config(config_dict)
    
    if not config_dict['transcription'].get('enable', True):
        logger.info("Transcription disabled in config")
        return None
    
    cache_path = get_cache_path(audio_path, config_dict)
    
    if config_dict['transcription'].get('reuse_existing', True) and \
       not config_dict['transcription'].get('force_new', False):
        cached = load_cached_transcript(cache_path)
        if cached:
            return cached['transcript']
    
    model = init_whisper()
    if model is None:
        logger.warning("Proceeding without transcription due to Whisper initialization failure")
        return None
    
    try:
        logger.info("Starting transcription...")
        result = model.transcribe(
            audio_path,
            verbose=True,
            language=config_dict['transcription'].get('language', 'en')
        )
        logger.info("Transcription completed successfully")
        
        if config_dict['transcription'].get('save_transcript', True):
            save_transcript(result, cache_path)
        
        return result
        
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}", exc_info=True)
        return None

from .text_utils import find_best_fuzzy_match, normalize_scores

def get_segment_importance(segment, config_dict):
    """Calculate importance score for a transcript segment"""
    try:
        text = segment.get('text', '').lower()
        score = 0.0
        
        weights = config_dict.get('analysis_weights', DEFAULT_CONFIG['analysis_weights'])
        weights = weights.get('transcript_features', DEFAULT_CONFIG['analysis_weights']['transcript_features'])
        
        if len(text) < 10:
            return 0.0
        
        # Get marker weights
        marker_weights = weights.get('marker_weights', {
            'important_phrases': 0.4,
            'topic_indicators': 0.4,
            'conclusion_markers': 0.2
        })
        
        markers = config_dict.get('content_markers', {})
        
        # Track all matches and scores
        matches = []
        
        # Analyze text with fuzzy matching
        threshold = config_dict.get('transcription', {}).get('fuzzy_match_threshold', 85)
        for phrase_list in ['important_phrases', 'topic_indicators', 'conclusion_markers']:
            phrases = markers.get(phrase_list, [])
            if not phrases:
                continue
                
            matched_phrase, match_score, context_score = find_best_fuzzy_match(text, phrases, threshold)
            if matched_phrase:
                weight = marker_weights.get(phrase_list, 0.0)
                # Combine similarity and context scores
                phrase_score = match_score * (1 + context_score)  # Context boosts base score
                matches.append({
                    'phrase': matched_phrase,
                    'type': phrase_list,
                    'score': phrase_score,
                    'weight': weight
                })
                logger.debug(f"Found {phrase_list} match '{matched_phrase}' with score {match_score:.1f}, context {context_score:.1f} (weight: {weight:.1f})")
                
        # Calculate final score incorporating all matches
        if matches:
            # Sum weighted scores
            weighted_scores = [m['score'] * m['weight'] for m in matches]
            # Normalize to handle multiple matches properly
            score = sum(normalize_scores(weighted_scores))
            
            # Boost score if multiple relevant matches found
            if len(matches) > 1:
                score *= (1 + 0.2 * (len(matches) - 1))  # 20% boost per additional match
        
        # Questions are now handled through markers.json
        # Add any additional analysis here if needed
        
        score = min(1.0, score)
        logger.debug(f"Segment importance score: {score:.2f}")
        return score
        
    except Exception as e:
        logger.error(f"Error calculating segment importance: {e}")
        return 0.0
