"""
Generate audio using Coqui TTS model with zero-shot voice cloning.
"""

import argparse
import time
import os
from pathlib import Path

from models import CoquiTTS
from utils import (
    ensure_directories,
    REFERENCE_DIR,
    get_audio_duration,
    load_audio
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate speech using Coqui TTS with voice cloning"
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
    """
    Find reference audio file.

    Args:
        reference_path: Optional path to reference audio

    Returns:
        Path to reference audio file

    Raises:
        FileNotFoundError: If no reference audio found
    """
    if reference_path:
        ref_path = Path(reference_path)
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference audio not found: {reference_path}")
        return ref_path

    # Search for first .wav file in REFERENCE_DIR
    wav_files = list(REFERENCE_DIR.glob("*.wav"))
    if not wav_files:
        raise FileNotFoundError(
            f"No .wav files found in {REFERENCE_DIR}. "
            "Please provide a reference audio file."
        )

    return wav_files[0]


def calculate_rtf(generation_time, audio_duration):
    """
    Calculate Real-Time Factor.

    RTF = generation_time / audio_duration
    RTF < 1 means faster than real-time

    Args:
        generation_time: Time taken to generate audio (seconds)
        audio_duration: Duration of generated audio (seconds)

    Returns:
        Real-Time Factor
    """
    if audio_duration == 0:
        return float('inf')
    return generation_time / audio_duration


def main():
    """
    Main execution function.

    Orchestrates:
    1. Parse arguments
    2. Ensure directories exist
    3. Find reference audio
    4. Initialize Coqui TTS model
    5. Generate audio with timing
    6. Calculate RTF
    7. Display results
    """
    # Parse arguments
    args = parse_args()

    print("=" * 60)
    print("Coqui TTS - Zero-Shot Voice Cloning")
    print("=" * 60)

    # Ensure directories exist
    ensure_directories()

    # Find reference audio
    print(f"\nText to generate: '{args.text}'")
    reference_audio_path = find_reference_audio(args.reference)
    print(f"Reference audio: {reference_audio_path}")

    # Initialize model
    print("\nInitializing Coqui TTS model...")
    model = CoquiTTS()

    # Generate audio with timing
    print("\nGenerating speech...")
    start_time = time.time()

    output_path = model.generate(
        text=args.text,
        reference_audio_path=reference_audio_path,
        output_path=Path(args.output) if args.output else None
    )

    generation_time = time.time() - start_time

    # Calculate RTF
    generated_audio, sr = load_audio(output_path)
    audio_duration = get_audio_duration(generated_audio, sr)
    rtf = calculate_rtf(generation_time, audio_duration)

    # Display results
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
