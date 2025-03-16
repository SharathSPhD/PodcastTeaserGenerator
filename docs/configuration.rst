Configuration
=============

The behavior of the Podcast Teaser Generator can be customized through a configuration file. By default, the application uses the settings in ``config.json``, but you can provide your own configuration file with the ``--config`` option.

Configuration File Format
------------------------

The configuration file is in JSON format. Here's an example with all available options:

.. code-block:: json

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
      
      "visualize": false,
      
      "transcription": {
        "enable": true,
        "method": "whisper",
        "keyword_boost": ["interesting", "amazing", "surprising"]
      }
    }

Configuration Parameters
----------------------

Basic Teaser Settings
~~~~~~~~~~~~~~~~~~~~

+------------------------+---------------------------------------------------+----------------+
| Parameter              | Description                                       | Default        |
+========================+===================================================+================+
| ``teaser_duration``    | Target duration in seconds for individual teasers | 60             |
+------------------------+---------------------------------------------------+----------------+
| ``segment_min_duration``| Minimum duration for each segment in seconds     | 3              |
+------------------------+---------------------------------------------------+----------------+
| ``segment_max_duration``| Maximum duration for each segment in seconds     | 15             |
+------------------------+---------------------------------------------------+----------------+
| ``num_segments``       | Target number of segments to extract              | 5              |
+------------------------+---------------------------------------------------+----------------+
| ``crossfade_duration`` | Duration of crossfade between segments in ms      | 500            |
+------------------------+---------------------------------------------------+----------------+
| ``output_format``      | Audio format for output files (mp3, wav, etc.)    | "mp3"          |
+------------------------+---------------------------------------------------+----------------+
| ``normalize_audio``    | Whether to normalize audio levels in final teaser | true           |
+------------------------+---------------------------------------------------+----------------+

Analysis Weights
~~~~~~~~~~~~~~

+------------------------+---------------------------------------------------+----------------+
| Parameter              | Description                                       | Default        |
+========================+===================================================+================+
| ``energy_weight``      | Weight for energy-based detection                 | 0.4            |
+------------------------+---------------------------------------------------+----------------+
| ``spectral_weight``    | Weight for spectral contrast (tonal variation)    | 0.3            |
+------------------------+---------------------------------------------------+----------------+
| ``tempo_weight``       | Weight for speech tempo variations                | 0.2            |
+------------------------+---------------------------------------------------+----------------+
| ``silence_threshold``  | dB threshold for silence detection                | -40            |
+------------------------+---------------------------------------------------+----------------+

Intro/Outro Handling
~~~~~~~~~~~~~~~~~~

+------------------------+---------------------------------------------------+----------------+
| Parameter              | Description                                       | Default        |
+========================+===================================================+================+
| ``exclude_intro_outro``| Whether to exclude podcast intro/outro music      | true           |
+------------------------+---------------------------------------------------+----------------+
| ``intro_duration``     | Estimated duration of intro in seconds            | 30             |
+------------------------+---------------------------------------------------+----------------+
| ``outro_duration``     | Estimated duration of outro in seconds            | 30             |
+------------------------+---------------------------------------------------+----------------+

Summary Teaser Settings
~~~~~~~~~~~~~~~~~~~~~

+---------------------------+---------------------------------------------------+----------------+
| Parameter                 | Description                                       | Default        |
+===========================+===================================================+================+
| ``create_summary_teaser`` | Create summary when processing multiple files     | true           |
+---------------------------+---------------------------------------------------+----------------+
| ``summary_segments_per_track``| Segments to include per track in summary      | 2              |
+---------------------------+---------------------------------------------------+----------------+
| ``summary_teaser_duration``| Target duration for summary teaser in seconds    | 120            |
+---------------------------+---------------------------------------------------+----------------+

Visualization
~~~~~~~~~~~~

+------------------------+---------------------------------------------------+----------------+
| Parameter              | Description                                       | Default        |
+========================+===================================================+================+
| ``visualize``          | Generate visualization of audio analysis          | false          |
+------------------------+---------------------------------------------------+----------------+

Transcription Settings
~~~~~~~~~~~~~~~~~~~~

+------------------------+---------------------------------------------------+----------------+
| Parameter              | Description                                       | Default        |
+========================+===================================================+================+
| ``transcription.enable``| Whether to use transcription-based analysis      | true           |
+------------------------+---------------------------------------------------+----------------+
| ``transcription.method``| Method to use ("whisper" or "sphinx")            | "whisper"      |
+------------------------+---------------------------------------------------+----------------+
| ``transcription.keyword_boost``| Keywords to boost in segment selection    | []             |
+------------------------+---------------------------------------------------+----------------+

Optimizing for Different Podcast Types
------------------------------------

Interview Podcasts
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "segment_min_duration": 5,
      "segment_max_duration": 15,
      "energy_weight": 0.3,
      "spectral_weight": 0.5,
      "tempo_weight": 0.2
    }

Solo Podcasts / Monologue
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "segment_min_duration": 3,
      "segment_max_duration": 10,
      "energy_weight": 0.5,
      "spectral_weight": 0.2,
      "tempo_weight": 0.3
    }

Storytelling Podcasts
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "segment_min_duration": 4,
      "segment_max_duration": 12,
      "energy_weight": 0.4,
      "spectral_weight": 0.3,
      "tempo_weight": 0.3
    }
