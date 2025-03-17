#!/usr/bin/env python3
"""
Test Installation Script for Podcast Teaser Generator

This script verifies that the Podcast Teaser Generator package 
has been installed correctly and all dependencies are available.
"""

import os
import sys
import subprocess
import importlib
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

def print_status(message, success=None):
    """Print a status message with optional success indicator."""
    if success is None:
        print(f"[*] {message}")
    elif success:
        print(f"[✓] {message}")
    else:
        print(f"[✗] {message}")

def check_python_version():
    """Check if Python version is compatible."""
    required_version = (3, 7)
    current_version = sys.version_info
    
    version_str = '.'.join(map(str, current_version[:3]))
    required_str = '.'.join(map(str, required_version))
    
    if current_version >= required_version:
        print_status(f"Python version {version_str} (>= {required_str})", True)
        return True
    else:
        print_status(f"Python version {version_str} (< {required_str} required)", False)
        return False

def check_package_installed():
    """Check if podcast-teaser package is installed."""
    try:
        import podcast_teaser
        version = getattr(podcast_teaser, '__version__', 'unknown')
        print_status(f"Podcast Teaser Generator installed (version: {version})", True)
        return True
    except ImportError:
        print_status("Podcast Teaser Generator not installed", False)
        return False

def check_dependencies():
    """Check if all dependencies are installed."""
    required_packages = [
        'numpy>=1.19.0',
        'scipy>=1.5.0',
        'librosa>=0.8.0',
        'pydub>=0.24.0',
        'matplotlib>=3.3.0',
        'soundfile>=0.10.0',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.require(package)
        except (DistributionNotFound, VersionConflict):
            missing_packages.append(package)
    
    if not missing_packages:
        print_status("All dependencies installed", True)
        return True
    else:
        print_status(f"Missing dependencies: {', '.join(missing_packages)}", False)
        return False

def check_audio_libs():
    """Check if system audio libraries are properly installed."""
    try:
        # Try to import and use librosa which depends on audio libraries
        import librosa
        import numpy as np
        
        # Create a small test array and try to process it
        test_array = np.zeros(1000)
        librosa.feature.rms(y=test_array)
        
        print_status("Audio processing libraries working correctly", True)
        return True
    except Exception as e:
        print_status(f"Audio processing libraries issue: {str(e)}", False)
        return False

def try_running_script():
    """Try to run the main script with --help flag."""
    try:
        # Try to find the main script
        script_paths = [
            "podcast_teaser.py",
            os.path.join("podcast_teaser", "podcast_teaser.py"),
            os.path.join("bin", "podcast_teaser")
        ]
        
        script_path = None
        for path in script_paths:
            if os.path.exists(path):
                script_path = path
                break
        
        if script_path is None:
            print_status("Main script not found", False)
            return False
            
        # Try to run with help flag
        result = subprocess.run([sys.executable, script_path, "--help"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("Main script executes correctly", True)
            return True
        else:
            print_status(f"Error running main script: {result.stderr}", False)
            return False
    except Exception as e:
        print_status(f"Exception running main script: {str(e)}", False)
        return False

def main():
    """Run all installation tests."""
    print("Podcast Teaser Generator - Installation Test")
    print("============================================")
    
    python_ok = check_python_version()
    package_ok = check_package_installed()
    deps_ok = check_dependencies()
    audio_ok = check_audio_libs()
    script_ok = try_running_script()
    
    print("\nTest Summary")
    print("-----------")
    all_ok = python_ok and package_ok and deps_ok and audio_ok and script_ok
    
    if all_ok:
        print("\n✅ Installation successful! The package is ready to use.")
        print("\nTo generate a teaser, run:")
        print("  python podcast_teaser.py path/to/your/podcast.mp3")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above before using the package.")
        print("For assistance, check the documentation or create an issue on GitHub.")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
