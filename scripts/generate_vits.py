"""
Generate audio using VITS model with zero-shot voice cloning.
"""

import argparse
import time
import os
from pathlib import Path

from models import VITS
from utils import (
    ensure_directories,
    REFERENCE_DIR,
    get_audio_duration,
    load_audio
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate speech using VITS with voice cloning"
    )

    # Get text from environment variable or argument
    default_text = os.environ.get('TEXT', 'Hello, this is a test of voice cloning.')

    parser.add_argument(
        '--text',
        type=str,
        default=default_text,
        help='Text to convert to speech'
    )
    parser.add_argument(
        '--reference',
        type=str,
        default=None,
        help='Path to reference audio file (optional, auto-detected if not provided)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output path for generated audio (optional, auto-generated if not provided)'
    )

    return parser.parse_args()


def find_reference_audio(reference_path=None):
    """Find reference audio file."""
    if reference_path:
        ref_path = Path(reference_path)
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference audio not found: {reference_path}")
        return ref_path

    # Search for audio files in REFERENCE_DIR
    audio_files = list(REFERENCE_DIR.glob("*.wav")) + list(REFERENCE_DIR.glob("*.mp3"))

    if not audio_files:
        raise FileNotFoundError(
            f"No audio files found in {REFERENCE_DIR}. "
            "Please provide a .wav or .mp3 file."
        )

    return audio_files[0]


def calculate_rtf(generation_time, audio_duration):
    """Calculate Real-Time Factor."""
    if audio_duration == 0:
        return float('inf')
    return generation_time / audio_duration


def main():
    """Main execution function."""
    args = parse_args()

    print("=" * 60)
    print("VITS - Zero-Shot Voice Cloning")
    print("=" * 60)

    ensure_directories()

    print(f"\nText to generate: '{args.text}'")
    reference_audio_path = find_reference_audio(args.reference)
    print(f"Reference audio: {reference_audio_path}")

    print("\nInitializing VITS model...")
    model = VITS()

    print("\nGenerating speech...")
    start_time = time.time()

    output_path = model.generate(
        text=args.text,
        reference_audio_path=reference_audio_path,
        output_path=Path(args.output) if args.output else None
    )

    generation_time = time.time() - start_time

    generated_audio, sr = load_audio(output_path)
    audio_duration = get_audio_duration(generated_audio, sr)
    rtf = calculate_rtf(generation_time, audio_duration)

    print("\n" + "=" * 60)
    print("Generation completed successfully!")
    print("=" * 60)
    print(f"Output: {output_path}")
    print(f"Audio duration: {audio_duration:.2f} seconds")
    print(f"Generation time: {generation_time:.2f} seconds")
    print(f"Real-Time Factor (RTF): {rtf:.2f}x")

    if rtf < 1:
        print(f"  → {1/rtf:.2f}x faster than real-time")
    elif rtf > 1:
        print(f"  → {rtf:.2f}x slower than real-time")
    else:
        print("  → Exactly real-time")

    print("=" * 60)


if __name__ == "__main__":
    main()
