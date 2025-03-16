"""
Tests for configuration handling
"""
import os
import pytest
import tempfile
import json

from src import config

def test_default_config_loading():
    """Test that default configuration loads properly"""
    # Load default config
    cfg = config.load_config(None)
    
    # Check some expected values
    assert 'teaser_duration' in cfg
    assert 'output_format' in cfg
    assert isinstance(cfg['teaser_duration'], int)
    assert isinstance(cfg['output_format'], str)

def test_custom_config_loading():
    """Test loading a custom configuration file"""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp:
        custom_config = {
            "teaser_duration": 90,
            "segment_min_duration": 5,
            "output_format": "wav"
        }
        json.dump(custom_config, temp)
        temp_path = temp.name
    
    try:
        # Load the custom config
        cfg = config.load_config(temp_path)
        
        # Check that custom values were loaded
        assert cfg['teaser_duration'] == 90
        assert cfg['segment_min_duration'] == 5
        assert cfg['output_format'] == 'wav'
        
        # Check that values not in custom config have defaults
        assert 'energy_weight' in cfg
        assert 'visualize' in cfg
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def test_config_validation():
    """Test configuration validation"""
    # TODO: Implement once validation is added to config module
    pass
