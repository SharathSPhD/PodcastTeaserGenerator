"""
Configuration settings and logging setup
"""

import logging
import os
import json
from datetime import datetime
from .defaults import DEFAULT_CONFIG

def setup_logging():
    """Set up logging configuration"""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    logger = logging.getLogger("podcast_teaser")
    logger.setLevel(logging.DEBUG)
    
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main_handler = logging.FileHandler(f"logs/podcast_teaser_{timestamp}.log")
    main_handler.setLevel(logging.DEBUG)
    main_handler.setFormatter(detailed_formatter)
    
    error_handler = logging.FileHandler(f"logs/podcast_teaser_errors_{timestamp}.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(main_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

# Set up logger
logger = setup_logging()

def load_config(config_path=None):
    """
    Load and validate configuration
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        dict: Configuration dictionary with defaults filled in
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path:
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                logger.info(f"Loaded user configuration from {config_path}")
                
                def update_recursive(base, new):
                    for key, value in new.items():
                        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                            update_recursive(base[key], value)
                        else:
                            base[key] = value
                
                update_recursive(config, user_config)
                logger.debug("User configuration merged with defaults")
        except Exception as e:
            logger.error(f"Error loading configuration from {config_path}: {e}")
            logger.info("Using default configuration")
    
    try:
        validate_config(config)
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        logger.info("Using default configuration")
        config = DEFAULT_CONFIG.copy()
    
    return config

def validate_config(config):
    """Validate configuration values"""
    required_fields = [
        "teaser_duration",
        "segment_min_duration",
        "segment_max_duration",
        "num_segments",
        "crossfade_duration"
    ]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required configuration field: {field}")
    
    if config["teaser_duration"] <= 0:
        raise ValueError("teaser_duration must be positive")
    if config["segment_min_duration"] <= 0:
        raise ValueError("segment_min_duration must be positive")
    if config["segment_max_duration"] <= config["segment_min_duration"]:
        raise ValueError("segment_max_duration must be greater than segment_min_duration")
    if config["num_segments"] <= 0:
        raise ValueError("num_segments must be positive")
    
    if "analysis_weights" in config:
        weights = config["analysis_weights"]
        if "transcript_importance" in weights and "audio_dynamics" in weights:
            if abs(weights["transcript_importance"] + weights["audio_dynamics"] - 1.0) > 0.01:
                raise ValueError("transcript_importance and audio_dynamics must sum to 1.0")
    
    logger.debug("Configuration validation successful")
