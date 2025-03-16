"""
Visualization utilities for podcast teaser analysis
"""

import matplotlib.pyplot as plt
from . import config
from .defaults import DEFAULT_CONFIG

logger = config.logger

def visualize_analysis(analysis_results, segments, output_prefix):
    """
    Create visualization of the audio analysis and selected segments
    
    Args:
        analysis_results: Analysis data from analyze_audio
        segments: Selected highlight segments
        output_prefix: Prefix for output files
    """
    logger.info("Generating visualization...")
    
    # Get all scores
    timestamps = analysis_results['timestamps']
    audio_score = analysis_results['audio_score']
    rms_norm = analysis_results['rms_norm']
    contrast_norm = analysis_results['contrast_norm']
    tempo_norm = analysis_results['tempo_norm']
    
    # Calculate transcript score if available
    transcript_score = None
    if 'transcript_segments' in analysis_results:
        from . import analysis
        transcript_score = analysis.get_transcript_score_array(
            analysis_results['transcript_segments'],
            len(audio_score),
            analysis_results['sr'],
            analysis_results['hop_length']
        )
    
    # Create figure
    plt.figure(figsize=(15, 12 if transcript_score is not None else 10))
    
    # Plot 1: Combined scores
    plt.subplot(5 if transcript_score is not None else 4, 1, 1)
    plt.plot(timestamps, audio_score, label='Audio Score', alpha=0.7)
    if transcript_score is not None:
        plt.plot(timestamps, transcript_score, label='Transcript Score', alpha=0.7)
    plt.title('Analysis Scores with Selected Segments')
    plt.ylabel('Score')
    plt.legend()
    
    # Highlight selected segments
    for start, end in segments:
        plt.axvspan(start, end, color='green', alpha=0.2)
    
    # Plot 2: RMS energy
    plt.subplot(5 if transcript_score is not None else 4, 1, 2)
    plt.plot(timestamps, rms_norm)
    plt.title('Normalized RMS Energy')
    plt.ylabel('Energy')
    
    # Plot 3: Spectral contrast
    plt.subplot(5 if transcript_score is not None else 4, 1, 3)
    plt.plot(timestamps, contrast_norm)
    plt.title('Normalized Spectral Contrast')
    plt.ylabel('Contrast')
    
    # Plot 4: Tempo changes
    plt.subplot(5 if transcript_score is not None else 4, 1, 4)
    plt.plot(timestamps, tempo_norm)
    plt.title('Normalized Tempo Changes')
    plt.ylabel('Tempo Change')
    
    # Plot 5: Transcript segments (if available)
    if transcript_score is not None:
        plt.subplot(5, 1, 5)
        plt.plot(timestamps, transcript_score)
        plt.title('Transcript Importance Score')
        plt.ylabel('Importance')
    
    plt.xlabel('Time (seconds)')
    plt.tight_layout()
    
    # Save plot
    viz_path = f"{output_prefix}_analysis.png"
    plt.savefig(viz_path)
    plt.close()
    
    logger.info(f"Visualization saved to {viz_path}")
