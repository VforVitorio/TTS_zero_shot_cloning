"""
Run all TTS models sequentially and compare results.
"""

import argparse
import time
import os
from pathlib import Path
from typing import Dict, Optional

from models import CoquiTTS, GPTSoVITS
from utils import (
    ensure_directories,
    REFERENCE_DIR,
    get_audio_duration,
    load_audio
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run all TTS models and compare results"
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

    Args:
        generation_time: Time taken to generate audio (seconds)
        audio_duration: Duration of generated audio (seconds)

    Returns:
        Real-Time Factor
    """
    if audio_duration == 0:
        return float('inf')
    return generation_time / audio_duration


def run_coqui_generation(text: str, reference_path: Path) -> Optional[Dict]:
    """
    Run Coqui TTS generation.

    Args:
        text: Text to synthesize
        reference_path: Path to reference audio

    Returns:
        Dictionary with results or None if failed
    """
    try:
        print("\n" + "=" * 60)
        print("Running Coqui TTS")
        print("=" * 60)

        # Initialize model
        print("Initializing Coqui TTS model...")
        model = CoquiTTS()

        # Generate audio with timing
        print("Generating speech...")
        start_time = time.time()
        output_path = model.generate(text=text, reference_audio_path=reference_path)
        generation_time = time.time() - start_time

        # Calculate metrics
        generated_audio, sr = load_audio(output_path)
        audio_duration = get_audio_duration(generated_audio, sr)
        rtf = calculate_rtf(generation_time, audio_duration)

        results = {
            'model': 'Coqui TTS',
            'output_path': str(output_path),
            'audio_duration': audio_duration,
            'generation_time': generation_time,
            'rtf': rtf,
            'success': True
        }

        print(f"✓ Coqui TTS completed in {generation_time:.2f}s (RTF: {rtf:.2f}x)")
        return results

    except Exception as e:
        print(f"✗ Coqui TTS failed: {str(e)}")
        return {
            'model': 'Coqui TTS',
            'success': False,
            'error': str(e)
        }


def run_gptsovits_generation(text: str, reference_path: Path) -> Optional[Dict]:
    """
    Run GPT-SoVITS generation.

    Args:
        text: Text to synthesize
        reference_path: Path to reference audio

    Returns:
        Dictionary with results or None if failed
    """
    try:
        print("\n" + "=" * 60)
        print("Running GPT-SoVITS")
        print("=" * 60)

        # Initialize model
        print("Initializing GPT-SoVITS model...")
        model = GPTSoVITS()

        # Generate audio with timing
        print("Generating speech...")
        start_time = time.time()
        output_path = model.generate(text=text, reference_audio_path=reference_path)
        generation_time = time.time() - start_time

        # Calculate metrics
        generated_audio, sr = load_audio(output_path)
        audio_duration = get_audio_duration(generated_audio, sr)
        rtf = calculate_rtf(generation_time, audio_duration)

        results = {
            'model': 'GPT-SoVITS',
            'output_path': str(output_path),
            'audio_duration': audio_duration,
            'generation_time': generation_time,
            'rtf': rtf,
            'success': True
        }

        print(f"✓ GPT-SoVITS completed in {generation_time:.2f}s (RTF: {rtf:.2f}x)")
        return results

    except NotImplementedError as e:
        print(f"⚠ GPT-SoVITS not implemented: {str(e)}")
        return {
            'model': 'GPT-SoVITS',
            'success': False,
            'error': 'Not implemented',
            'note': 'GPT-SoVITS requires additional setup'
        }
    except Exception as e:
        print(f"✗ GPT-SoVITS failed: {str(e)}")
        return {
            'model': 'GPT-SoVITS',
            'success': False,
            'error': str(e)
        }


def display_comparison(results: list):
    """
    Display comparison table of results.

    Args:
        results: List of result dictionaries from each model
    """
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)

    # Filter successful results
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]

    if successful:
        print("\nSuccessful generations:")
        print("-" * 60)
        print(f"{'Model':<20} {'Duration':<12} {'Gen Time':<12} {'RTF':<10}")
        print("-" * 60)

        for result in successful:
            model = result['model']
            duration = f"{result['audio_duration']:.2f}s"
            gen_time = f"{result['generation_time']:.2f}s"
            rtf = f"{result['rtf']:.2f}x"
            print(f"{model:<20} {duration:<12} {gen_time:<12} {rtf:<10}")

        # Find fastest model
        if len(successful) > 1:
            fastest = min(successful, key=lambda x: x['rtf'])
            print("-" * 60)
            print(f"Fastest model: {fastest['model']} (RTF: {fastest['rtf']:.2f}x)")

    if failed:
        print("\nFailed generations:")
        print("-" * 60)
        for result in failed:
            model = result['model']
            error = result.get('error', 'Unknown error')
            note = result.get('note', '')
            print(f"✗ {model}: {error}")
            if note:
                print(f"  Note: {note}")

    print("=" * 60)


def main():
    """
    Main execution function.

    Orchestrates:
    1. Parse arguments
    2. Ensure directories exist
    3. Find reference audio
    4. Run all models sequentially
    5. Display comparison
    """
    # Parse arguments
    args = parse_args()

    print("=" * 60)
    print("TTS Model Comparison - Zero-Shot Voice Cloning")
    print("=" * 60)

    # Ensure directories exist
    ensure_directories()

    # Find reference audio
    print(f"\nText to generate: '{args.text}'")
    reference_audio_path = find_reference_audio(args.reference)
    print(f"Reference audio: {reference_audio_path}")

    # Run all models
    results = []

    # Run Coqui TTS
    coqui_result = run_coqui_generation(args.text, reference_audio_path)
    if coqui_result:
        results.append(coqui_result)

    # Run GPT-SoVITS
    gptsovits_result = run_gptsovits_generation(args.text, reference_audio_path)
    if gptsovits_result:
        results.append(gptsovits_result)

    # Display comparison
    display_comparison(results)


if __name__ == "__main__":
    main()
