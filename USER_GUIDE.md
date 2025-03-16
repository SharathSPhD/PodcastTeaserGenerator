# Podcast Teaser Generator - User Guide

## Introduction

This guide explains how to use the Podcast Teaser Generator to automatically create engaging audio teasers from your podcast episodes. The tool uses audio analysis to identify and extract the most interesting segments from your podcast tracks and combine them into professional-sounding teasers.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Command Line Options](#command-line-options)
4. [Configuration Parameters](#configuration-parameters)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Installation

1. Clone or download the repository
2. Install dependencies:
```
pip install -r requirements.txt
```

## Basic Usage

### Generate a teaser from a single podcast

```
python podcast_teaser.py path/to/your/podcast.mp3
```

The teaser will be saved to the `output_teasers` directory by default.

### Process all podcast files in a directory

```
python podcast_teaser.py path/to/podcast/directory
```

### Using the convenience scripts

#### Windows
```
run_teaser.bat path/to/podcast.mp3 60 visualize exclude-intro-outro create-summary
```

#### Linux/macOS
```
./run_teaser.sh path/to/podcast.mp3 60 visualize exclude-intro-outro create-summary
```

Where:
- First parameter: Input file or directory
- Second parameter: Target duration in seconds
- Third parameter: Use "visualize" to generate visualizations
- Fourth parameter: Use "exclude-intro-outro" to ignore intro/outro music
- Fifth parameter: Use "create-summary" to generate a summary teaser

## Command Line Options

```
python podcast_teaser.py [input] [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--output-dir`, `-o` | Output directory (default: output_teasers) |
| `--config`, `-c` | Path to custom configuration file |
| `--visualize`, `-v` | Generate visualization of audio analysis |
| `--duration`, `-d` | Target teaser duration in seconds (default: 60) |
| `--summary`, `-s` | Create a summary teaser (when processing multiple files) |
| `--no-intro-outro`, `-n` | Exclude intro and outro sections from teasers |

## Configuration Parameters

The behavior of the teaser generator can be customized by editing the `config.json` file or providing your own configuration file with the `--config` option.

### Basic Teaser Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `teaser_duration` | Target duration in seconds for individual teasers | 60 |
| `segment_min_duration` | Minimum duration for each extracted segment in seconds | 3 |
| `segment_max_duration` | Maximum duration for each extracted segment in seconds | 15 |
| `num_segments` | Target number of segments to extract for each teaser | 5 |
| `crossfade_duration` | Duration of crossfade between segments in milliseconds | 500 |
| `output_format` | Audio format for output files (mp3, wav, etc.) | "mp3" |
| `normalize_audio` | Whether to normalize audio levels in final teaser | true |

### Analysis Weights

These weights control how different audio features influence segment selection:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `energy_weight` | Weight for energy-based detection (louder/excited moments) | 0.4 |
| `spectral_weight` | Weight for spectral contrast (tonal variation) | 0.3 |
| `tempo_weight` | Weight for speech tempo variations | 0.2 |
| `silence_threshold` | dB threshold for silence detection | -40 |

**Note**: Weights should sum to approximately 1.0 for best results.

### Intro/Outro Handling

| Parameter | Description | Default |
|-----------|-------------|---------|
| `exclude_intro_outro` | Whether to exclude podcast intro/outro music | true |
| `intro_duration` | Estimated duration of intro in seconds | 30 |
| `outro_duration` | Estimated duration of outro in seconds | 30 |

### Summary Teaser Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `create_summary_teaser` | Whether to create a summary teaser when processing multiple files | true |
| `summary_segments_per_track` | Number of segments to include per track in summary | 2 |
| `summary_teaser_duration` | Target duration for summary teaser in seconds | 120 |

### Visualization

| Parameter | Description | Default |
|-----------|-------------|---------|
| `visualize` | Whether to generate visualization of audio analysis | false |

## Best Practices

### Optimizing Teaser Quality

1. **Adjust segment durations based on your content**:
   - Interview podcasts: Use longer segments (5-15 seconds) to capture complete thoughts
   - Solo podcasts: Shorter segments (3-8 seconds) can work well
   - Multiple hosts: Medium segments (4-10 seconds) to capture interactions

2. **Customize weights based on your podcast style**:
   - Dynamic conversations: Increase `energy_weight` to catch excited moments
   - Educational content: Increase `spectral_weight` to catch explanations
   - Storytelling: Balance weights or slightly increase `tempo_weight`

3. **Intro/Outro Handling**:
   - Measure your actual intro/outro duration and set those values
   - For cold opens before your intro music, use 0 for `intro_duration`
   - If you have mid-roll ads, try to place them after complete topics

### Batch Processing

1. Organize your podcast episodes in a single directory
2. Run the generator on the whole directory
3. Take advantage of the summary teaser feature to create "best of" compilations

### When to Use Visualization

Enable visualization (`--visualize` or `"visualize": true`) when:
- You're fine-tuning your configuration
- Your teasers aren't capturing the best moments
- You want to understand why certain segments were selected

## Troubleshooting

### Common Issues

1. **Teaser includes intro/outro music**
   - Increase `intro_duration` and `outro_duration` values
   - Verify `exclude_intro_outro` is set to `true`

2. **Segments cut off mid-sentence**
   - Increase `segment_min_duration` and `segment_max_duration`
   - Adjust `silence_threshold` if your podcast has background noise

3. **Teaser isn't capturing the most interesting moments**
   - Try adjusting the weights (`energy_weight`, `spectral_weight`, `tempo_weight`)
   - Use visualization to see what's being detected
   - For interview podcasts, increase `spectral_weight`

4. **Audio quality issues in final teaser**
   - Ensure `normalize_audio` is set to `true`
   - Try increasing `crossfade_duration` for smoother transitions
   - Use higher quality input files

### Error Messages

| Error | Solution |
|-------|----------|
| "No audio files found" | Check that your input directory contains supported audio files (.mp3, .wav, etc.) |
| "Error loading audio file" | Verify the file is not corrupted and is a supported format |
| "No segments found" | Try decreasing `silence_threshold` or adjusting weights |
