#!/usr/bin/env python3
"""
Podcast Teaser Generator
------------------------
Automatically creates engaging teasers from podcast audio tracks by 
identifying and extracting the most interesting segments based on audio analysis.
"""

import os
import argparse
import time
import json
from datetime import datetime
from tqdm import tqdm

from src import config
from src.generator import process_podcast, create_summary_teaser

def main():
    """
    Main function to parse arguments and process podcasts
    """
    # Set up logging
    logger = config.logger
    
    parser = argparse.ArgumentParser(description='Generate teasers from podcast audio')
    parser.add_argument('input', help='Input podcast file or directory containing podcast files')
    parser.add_argument('--output-dir', '-o', default='output_teasers', 
                        help='Directory to save teasers (default: output_teasers)')
    parser.add_argument('--config', '-c', help='Path to JSON configuration file')
    parser.add_argument('--markers', '-m', help='Path to content markers JSON file')
    parser.add_argument('--visualize', '-v', action='store_true', 
                        help='Generate visualization of audio analysis')
    parser.add_argument('--duration', '-d', type=int, default=60,
                        help='Target teaser duration in seconds (default: 60)')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='Create a summary teaser from all processed tracks')
    parser.add_argument('--no-intro-outro', '-n', action='store_true',
                        help='Exclude intro and outro sections from teasers')
    parser.add_argument('--no-transcription', action='store_true',
                        help='Disable transcription-based analysis')
    
    args = parser.parse_args()
    
    try:
        # Load base configuration
        cfg = config.load_config(args.config)
        
        # Load content markers if provided
        if args.markers:
            try:
                with open(args.markers, 'r') as f:
                    markers = json.load(f)
                    cfg['content_markers'] = markers
                    logger.info(f"Loaded content markers from {args.markers}")
            except Exception as e:
                logger.error(f"Error loading content markers: {e}")
                logger.info("Using default content markers")
        
        # Update config with command line arguments
        cfg['teaser_duration'] = args.duration
        cfg['visualize'] = args.visualize
        cfg['create_summary_teaser'] = args.summary or cfg.get('create_summary_teaser', True)
        if args.no_intro_outro:
            cfg['exclude_intro_outro'] = True
        if args.no_transcription:
            if 'transcription' in cfg:
                cfg['transcription']['enable'] = False
        
        # Ensure output directory exists
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Process input
        start_time = time.time()
        created_teasers = []
        
        if os.path.isfile(args.input):
            # Process single file
            try:
                teaser_path = process_podcast(args.input, args.output_dir, cfg)
                if teaser_path:
                    logger.info(f"Teaser created: {teaser_path}")
                    created_teasers.append(teaser_path)
            except Exception as e:
                logger.error(f"Error processing {args.input}: {str(e)}", exc_info=True)
        
        elif os.path.isdir(args.input):
            # Process all audio files in directory
            audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac']
            files = []
            for filename in os.listdir(args.input):
                if any(filename.lower().endswith(ext) for ext in audio_extensions):
                    files.append(os.path.join(args.input, filename))
            
            if not files:
                logger.error(f"No audio files found in {args.input}")
                return
            
            logger.info(f"Found {len(files)} audio files to process")
            
            for file in tqdm(files, desc="Processing files"):
                try:
                    teaser_path = process_podcast(file, args.output_dir, cfg)
                    if teaser_path:
                        logger.info(f"Teaser created: {teaser_path}")
                        created_teasers.append(teaser_path)
                except Exception as e:
                    logger.error(f"Error processing {file}: {str(e)}", exc_info=True)
                    continue
        else:
            logger.error(f"Input path does not exist: {args.input}")
            return
        
        # Create summary teaser if configured and multiple teasers were created
        if cfg.get('create_summary_teaser', True) and len(created_teasers) > 1:
            logger.info("Creating summary teaser from all processed tracks...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_path = os.path.join(args.output_dir, f"summary_teaser_{timestamp}.{cfg['output_format']}")
            
            try:
                summary_path = create_summary_teaser(created_teasers, summary_path, cfg)
                if summary_path:
                    logger.info(f"Summary teaser created: {summary_path}")
            except Exception as e:
                logger.error(f"Error creating summary teaser: {str(e)}", exc_info=True)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Processing completed in {elapsed_time:.2f} seconds")
        logger.info(f"Created {len(created_teasers)} individual teasers")
        
        # Print summary of what was created
        if created_teasers:
            logger.info("\nTeasers created:")
            for teaser in created_teasers:
                logger.info(f" - {os.path.basename(teaser)}")
                
            if cfg.get('create_summary_teaser', True) and len(created_teasers) > 1 and summary_path:
                logger.info(f"\nSummary teaser: {os.path.basename(summary_path)}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
