# Podcast Teaser Generator

Automatically generate engaging audio teasers from your podcast episodes.

## Overview

This tool analyzes your podcast audio tracks and automatically extracts the most interesting segments to create short, compelling teasers. It uses advanced audio analysis to identify segments with:

- High energy/excitement (volume peaks)
- Dynamic tonal variation (spectral contrast)
- Interesting speech rhythm patterns
- Clean cut points at natural breaks

## Features

- Fully automated teaser generation
- Customizable teaser duration and settings
- Smart segment selection based on audio features
- Clean transitions with automatic crossfades
- Audio level normalization
- Optional visualization of audio analysis
- Batch processing of multiple files

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/podcast_teaser.git
cd podcast_teaser
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Or install the package:
```
pip install -e .
```

## Usage

### Basic Usage

Generate a 60-second teaser from a podcast episode:

```
python podcast_teaser.py path/to/your/podcast.mp3
```

### Advanced Options

```
python podcast_teaser.py path/to/your/podcast.mp3 --duration 90 --visualize --output-dir custom_output
```

Process all podcast files in a directory:

```
python podcast_teaser.py path/to/podcast/directory --config custom_config.json
```

### Configuration

Customize the teaser generation by editing `config.json` or providing your own configuration file. The application uses the following configuration parameters:

#### Basic Teaser Settings
```json
{
  "teaser_duration": 60,            // Target duration in seconds for individual teasers
  "segment_min_duration": 3,        // Minimum duration for each extracted segment in seconds
  "segment_max_duration": 15,       // Maximum duration for each extracted segment in seconds
  "num_segments": 5,                // Target number of segments to extract for each teaser
  "crossfade_duration": 500,        // Duration of crossfade between segments in milliseconds
  "output_format": "mp3",           // Audio format for output files (mp3, wav, etc.)
  "normalize_audio": true,          // Whether to normalize audio levels in final teaser

  // Analysis weights - controls how segments are selected
  "energy_weight": 0.4,             // Weight for energy-based detection (louder/excited moments)
  "spectral_weight": 0.3,           // Weight for spectral contrast (tonal variation)
  "tempo_weight": 0.2,              // Weight for speech tempo variations
  "silence_threshold": -40,         // dB threshold for silence detection

  // Intro/Outro Handling
  "exclude_intro_outro": true,      // Whether to exclude podcast intro/outro music
  "intro_duration": 30,             // Estimated duration of intro in seconds
  "outro_duration": 30,             // Estimated duration of outro in seconds

  // Summary Teaser Settings
  "create_summary_teaser": true,    // Whether to create a summary teaser when processing multiple files
  "summary_segments_per_track": 2,  // Number of segments to include per track in summary
  "summary_teaser_duration": 120,   // Target duration for summary teaser in seconds

  // Visualization
  "visualize": false                // Whether to generate visualization of audio analysis
}
```

#### Configuration Details

**Basic Teaser Settings**
- `teaser_duration`: Controls how long the generated teaser will be. Shorter teasers will be more selective.
- `segment_min/max_duration`: Limits how short or long extracted segments can be. Adjust based on your content.
- `num_segments`: Target number of highlights to extract. The actual number may be less if not enough quality segments are found.
- `crossfade_duration`: Longer values create smoother transitions but may cut into content.

**Analysis Weights**
- `energy_weight`: Higher values favor louder, more excited moments.
- `spectral_weight`: Higher values favor segments with more vocal variation (questions, tonal shifts).
- `tempo_weight`: Higher values favor segments with changing speech rhythms.
- Weights should sum to approximately 1.0 for best results.

**Intro/Outro Handling**
- When `exclude_intro_outro` is enabled, the specified durations at the beginning and end of episodes are ignored during analysis.
- Adjust `intro_duration` and `outro_duration` to match your podcast format.

**Summary Teaser**
- When processing multiple episodes, a summary teaser combines the best moments from all episodes.
- `summary_segments_per_track` controls how many segments from each episode are considered.
- This feature is ideal for creating "best of" compilations from multiple episodes.

## How It Works

1. **Audio Analysis**: The system analyzes your podcast using multiple audio features:
   - RMS energy (volume/excitement)
   - Spectral contrast (tonal variation)
   - Speech tempo and rhythm patterns
   - Silence detection for natural breaks

2. **Segment Selection**: The most interesting moments are identified and scored.

3. **Smart Extraction**: Segments are intelligently extracted with clean cut points at natural breaks.

4. **Teaser Assembly**: Selected segments are combined with smooth crossfades.

5. **Output**: The final teaser is saved with optional visualization of the analysis.

## Example Visualization

When using the `--visualize` option, the system generates plots showing:
- Combined interest score with highlighted selected segments
- RMS energy analysis
- Spectral contrast analysis
- Tempo/rhythm analysis

## Tips for Better Results

- Longer episodes provide more material for selection
- Episodes with dynamic conversations tend to produce better teasers
- Try adjusting weights in config.json if teasers aren't capturing the right moments
- For interview podcasts, increasing the spectral_weight can help catch back-and-forth dialogue

## Documentation

Full documentation is available at [Read the Docs](https://podcast-teaser.readthedocs.io/).

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed with ❤️ for podcast creators everywhere.
