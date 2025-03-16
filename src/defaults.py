"""
Default configuration settings
"""

DEFAULT_CONFIG = {
    # Basic teaser settings
    "teaser_duration": 60,
    "segment_min_duration": 5,
    "segment_max_duration": 20,
    "num_segments": 5,
    "crossfade_duration": 500,
    "output_format": "mp3",
    "normalize_audio": True,
    "visualize": False,
    
    # Basic audio analysis weights
    "energy_weight": 0.4,
    "spectral_weight": 0.3,
    "tempo_weight": 0.3,
    "silence_threshold": -40,
    
    # Intro/Outro settings
    "exclude_intro_outro": True,
    "intro_duration": 30,
    "outro_duration": 30,
    
    # Summary settings
    "create_summary_teaser": True,
    "summary_segments_per_track": 2,
    "summary_teaser_duration": 120,
    
    # Transcription settings
    "transcription": {
        "enable": True,
        "model": "base",
        "language": "en",
        "cache_dir": "transcripts",
        "reuse_existing": True,
        "force_new": False,
        "save_transcript": True
    },
    
    # Analysis weights
    "analysis_weights": {
        "transcript_importance": 0.6,
        "audio_dynamics": 0.4,
        "transcript_features": {
            "marker_weights": {
                "important_phrases": 0.4,
                "topic_indicators": 0.4,
                "conclusion_markers": 0.2
            }
        },
        "audio_features": {
            "energy_weight": 0.4,
            "spectral_weight": 0.3,
            "tempo_weight": 0.3
        }
    }
}
