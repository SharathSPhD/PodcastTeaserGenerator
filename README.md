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

### From PyPI (Recommended)

The easiest way to install Podcast Teaser Generator is through PyPI:

```
pip install podcast-teaser
```

You can also specify a version:

```
pip install podcast-teaser==0.1.0
```

### From Source

If you prefer to install from source:

1. Clone this repository:
```
git clone https://github.com/SharathSPhD/PodcastTeaserGenerator.git
cd podcast_teaser
```

2. Install the package:
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
  "teaser_duration": 60,
  "segment_min_duration": 3,
  "segment_max_duration": 15,
  "num_segments": 5,
  "crossfade_duration": 500,
  "output_format": "mp3",
  "normalize_audio": true,

  "energy_weight": 0.4,
  "spectral_weight": 0.3,
  "tempo_weight": 0.2,
  "silence_threshold": -40,

  "exclude_intro_outro": true,
  "intro_duration": 30,
  "outro_duration": 30,

  "create_summary_teaser": true,
  "summary_segments_per_track": 2,
  "summary_teaser_duration": 120,

  "visualize": false
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
