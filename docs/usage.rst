Usage
=====

Basic Usage
----------

Generate a 60-second teaser from a podcast episode:

.. code-block:: bash

    python podcast_teaser.py path/to/your/podcast.mp3

This will create a teaser in the default ``output_teasers`` directory.

Command Line Options
------------------

.. code-block:: bash

    python podcast_teaser.py [input] [options]

Options
~~~~~~~

+------------------------+---------------------------------------------------+
| Option                 | Description                                       |
+========================+===================================================+
| ``--output-dir``, ``-o``| Output directory (default: output_teasers)       |
+------------------------+---------------------------------------------------+
| ``--config``, ``-c``   | Path to custom configuration file                 |
+------------------------+---------------------------------------------------+
| ``--visualize``, ``-v``| Generate visualization of audio analysis          |
+------------------------+---------------------------------------------------+
| ``--duration``, ``-d`` | Target teaser duration in seconds (default: 60)   |
+------------------------+---------------------------------------------------+
| ``--summary``, ``-s``  | Create a summary teaser (for multiple files)      |
+------------------------+---------------------------------------------------+
| ``--no-intro-outro``, ``-n`` | Exclude intro and outro sections            |
+------------------------+---------------------------------------------------+
| ``--no-transcription`` | Disable transcription-based analysis              |
+------------------------+---------------------------------------------------+

Advanced Usage Examples
---------------------

Generate a 90-second teaser with visualization:

.. code-block:: bash

    python podcast_teaser.py path/to/your/podcast.mp3 --duration 90 --visualize

Process all podcast files in a directory:

.. code-block:: bash

    python podcast_teaser.py path/to/podcast/directory --config custom_config.json

Generate a teaser, excluding intro and outro sections:

.. code-block:: bash

    python podcast_teaser.py path/to/your/podcast.mp3 --no-intro-outro

Using Convenience Scripts
-----------------------

For Windows:

.. code-block:: bash

    run_teaser.bat path/to/podcast.mp3 60 visualize exclude-intro-outro create-summary

For Linux/macOS:

.. code-block:: bash

    ./run_teaser.sh path/to/podcast.mp3 60 visualize exclude-intro-outro create-summary

Parameters:
  1. Input file or directory
  2. Target duration in seconds
  3. Use "visualize" to generate visualizations
  4. Use "exclude-intro-outro" to ignore intro/outro music
  5. Use "create-summary" to generate a summary teaser
