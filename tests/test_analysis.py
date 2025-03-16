"""
Tests for audio analysis functionality
"""
import pytest
import numpy as np

from src import analysis

def test_empty_audio():
    """Test handling of empty audio data"""
    # Create empty audio data
    y = np.array([])
    sr = 22050
    
    # Test with appropriate error handling
    with pytest.raises(ValueError):
        analysis.analyze_audio(y, sr, {})

def test_find_highlight_segments():
    """Test segment finding with mock analysis results"""
    # Mock analysis results
    mock_results = {
        'duration': 60.0,
        'sr': 22050,
        'interest_scores': np.array([0.1, 0.2, 0.9, 0.8, 0.7, 0.2, 0.1, 0.3, 0.4, 0.2]),
        'times': np.linspace(0, 60, 10),
        'silence_mask': np.array([False, False, False, False, False, False, False, False, False, False])
    }
    
    # Mock config with simple settings
    mock_config = {
        'teaser_duration': 20,
        'segment_min_duration': 5,
        'segment_max_duration': 10,
        'num_segments': 2
    }
    
    # Find segments
    segments = analysis.find_highlight_segments(mock_results, mock_config)
    
    # Basic validation
    assert isinstance(segments, list)
    assert len(segments) <= mock_config['num_segments']
    
    # Each segment should be a tuple of (start, end)
    for segment in segments:
        assert isinstance(segment, tuple)
        assert len(segment) == 2
        assert segment[0] < segment[1]
        
        # Duration should be within limits
        duration = segment[1] - segment[0]
        assert duration >= mock_config['segment_min_duration']
        assert duration <= mock_config['segment_max_duration']
