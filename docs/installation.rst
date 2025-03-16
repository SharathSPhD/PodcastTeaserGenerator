Installation
============

Requirements
-----------

Podcast Teaser Generator requires Python 3.7 or later and several dependencies for audio processing and analysis.

From PyPI
---------

The package can be installed from PyPI:

.. code-block:: bash

    pip install podcast-teaser

From Source
----------

You can also install directly from the source code:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/yourusername/podcast_teaser.git
       cd podcast_teaser

2. Install the package and its dependencies:

   .. code-block:: bash

       pip install -e .

   Or, to install just the dependencies:

   .. code-block:: bash

       pip install -r requirements.txt

Dependencies
-----------

The major dependencies include:

- **librosa**: For audio analysis
- **pydub**: For audio manipulation
- **numpy**: For numerical operations
- **matplotlib**: For visualization
- **SpeechRecognition** or **openai-whisper**: For transcription (optional)

Operating System Compatibility
-----------------------------

Podcast Teaser Generator works on:

- Windows
- macOS
- Linux

For Windows and macOS users, the included batch files and shell scripts provide an easy way to run the tool without remembering command line arguments.
