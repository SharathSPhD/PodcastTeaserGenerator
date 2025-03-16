@echo off
REM Podcast Teaser Generator Batch Script
REM Usage: run_teaser.bat [input_file_or_directory] [duration] [visualize] [exclude_intro_outro] [create_summary]

echo Podcast Teaser Generator
echo -----------------------

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Set default input path if not provided
set INPUT_PATH=%1
if "%INPUT_PATH%"=="" (
    set INPUT_PATH=input_tracks
    echo No input specified. Using default: %INPUT_PATH%
)

REM Set duration if provided (default: 60)
set DURATION=60
if not "%2"=="" (
    set DURATION=%2
)

REM Set visualization flag
set VISUALIZE=
if "%3"=="visualize" (
    set VISUALIZE=--visualize
)

REM Set exclude intro/outro flag
set INTRO_OUTRO=
if "%4"=="exclude-intro-outro" (
    set INTRO_OUTRO=--no-intro-outro
)

REM Set summary flag
set SUMMARY=
if "%5"=="create-summary" (
    set SUMMARY=--summary
)

REM Check if input exists
if not exist %INPUT_PATH% (
    echo Error: Input path "%INPUT_PATH%" does not exist
    exit /b 1
)

REM Create output directory if it doesn't exist
if not exist output_teasers (
    mkdir output_teasers
    echo Created output directory: output_teasers
)

REM Run the teaser generator
echo Running podcast teaser generator...
echo Input: %INPUT_PATH%
echo Duration: %DURATION% seconds
echo Visualization: %VISUALIZE%
echo Exclude Intro/Outro: %INTRO_OUTRO%
echo Create Summary: %SUMMARY%
echo.

python podcast_teaser.py %INPUT_PATH% --duration %DURATION% %VISUALIZE% %INTRO_OUTRO% %SUMMARY% --output-dir output_teasers --config config.json

if %ERRORLEVEL% neq 0 (
    echo Error occurred during processing.
) else (
    echo.
    echo Processing complete! Teasers saved to output_teasers directory.
)

echo.
pause
