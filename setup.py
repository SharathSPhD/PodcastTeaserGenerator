#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="podcast_teaser",
    version="0.1.0",
    author="Podcast Teaser Generator Contributors",
    author_email="example@example.com",
    description="Automatically generate engaging audio teasers from podcast episodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SharathSPhD/PodcastTeaserGenerator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
    ],
    python_requires=">=3.7",
    install_requires=[
        "librosa",
        "pydub",
        "numpy",
        "matplotlib",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "podcast-teaser=podcast_teaser:main",
        ],
    },
    include_package_data=True,
)
