"""
Enhanced logging configuration for podcast teaser
"""

import logging
import os
from datetime import datetime

def setup_logger():
    """
    Set up logger with both file and console handlers
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create timestamp for log files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set up main logger
    logger = logging.getLogger("podcast_teaser")
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler for all logs
    main_handler = logging.FileHandler(f"logs/podcast_teaser_{timestamp}.log")
    main_handler.setLevel(logging.DEBUG)
    main_handler.setFormatter(detailed_formatter)
    
    # Separate file handler for errors
    error_handler = logging.FileHandler(f"logs/podcast_teaser_errors_{timestamp}.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(main_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger
