"""
Run all TTS models sequentially and compare results.
"""

import argparse
import time
import os
from pathlib import Path
from typing import Dict, Optional

from models import YourTTS, XTTS, VITS
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

    # Search for audio files in REFERENCE_DIR
    audio_files = list(REFERENCE_DIR.glob("*.wav")) + list(REFERENCE_DIR.glob("*.mp3"))

    if not audio_files:
        raise FileNotFoundError(
            f"No audio files found in {REFERENCE_DIR}. "
            "Please provide a .wav or .mp3 file."
        )

    return audio_files[0]


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


def run_yourtts_generation(text: str, reference_path: Path) -> Optional[Dict]:
    """
    Run YourTTS generation.

    Args:
        text: Text to synthesize
        reference_path: Path to reference audio

    Returns:
        Dictionary with results or None if failed
    """
    try:
        print("\n" + "=" * 60)
        print("Running YourTTS")
        print("=" * 60)

        # Initialize model
        print("Initializing YourTTS model...")
        model = YourTTS()

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
            'model': 'YourTTS',
            'output_path': str(output_path),
            'audio_duration': audio_duration,
            'generation_time': generation_time,
            'rtf': rtf,
            'success': True
        }

        print(f"✓ YourTTS completed in {generation_time:.2f}s (RTF: {rtf:.2f}x)")
        return results

    except Exception as e:
        print(f"✗ YourTTS failed: {str(e)}")
        return {
            'model': 'YourTTS',
            'success': False,
            'error': str(e)
        }


def run_xtts_generation(text: str, reference_path: Path) -> Optional[Dict]:
    """
    Run XTTS v2 generation.

    Args:
        text: Text to synthesize
        reference_path: Path to reference audio

    Returns:
        Dictionary with results or None if failed
    """
    try:
        print("\n" + "=" * 60)
        print("Running XTTS v2")
        print("=" * 60)

        # Initialize model
        print("Initializing XTTS v2 model...")
        model = XTTS()

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
            'model': 'XTTS v2',
            'output_path': str(output_path),
            'audio_duration': audio_duration,
            'generation_time': generation_time,
            'rtf': rtf,
            'success': True
        }

        print(f"✓ XTTS v2 completed in {generation_time:.2f}s (RTF: {rtf:.2f}x)")
        return results

    except Exception as e:
        print(f"✗ XTTS v2 failed: {str(e)}")
        return {
            'model': 'XTTS v2',
            'success': False,
            'error': str(e)
        }


def run_vits_generation(text: str, reference_path: Path) -> Optional[Dict]:
    """
    Run VITS generation.

    Args:
        text: Text to synthesize
        reference_path: Path to reference audio

    Returns:
        Dictionary with results or None if failed
    """
    try:
        print("\n" + "=" * 60)
        print("Running VITS")
        print("=" * 60)

        # Initialize model
        print("Initializing VITS model...")
        model = VITS()

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
            'model': 'VITS',
            'output_path': str(output_path),
            'audio_duration': audio_duration,
            'generation_time': generation_time,
            'rtf': rtf,
            'success': True
        }

        print(f"✓ VITS completed in {generation_time:.2f}s (RTF: {rtf:.2f}x)")
        return results

    except Exception as e:
        print(f"✗ VITS failed: {str(e)}")
        return {
            'model': 'VITS',
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

    # Run YourTTS
    yourtts_result = run_yourtts_generation(args.text, reference_audio_path)
    if yourtts_result:
        results.append(yourtts_result)

    # Run XTTS v2
    xtts_result = run_xtts_generation(args.text, reference_audio_path)
    if xtts_result:
        results.append(xtts_result)

    # Run VITS
    vits_result = run_vits_generation(args.text, reference_audio_path)
    if vits_result:
        results.append(vits_result)

    # Display comparison
    display_comparison(results)

    # Save results to JSON file
    save_results_to_json(results, args.text, reference_audio_path)


def save_results_to_json(results: list, text: str, reference_audio_path: Path):
    """
    Save results to JSON file for later analysis.

    Args:
        results: List of result dictionaries from each model
        text: Text that was synthesized
        reference_audio_path: Path to reference audio used
    """
    import json
    import datetime

    # Create results directory if it doesn't exist
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Prepare output data
    output_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "text": text,
        "reference_audio": str(reference_audio_path),
        "models": results
    }

    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = results_dir / f"metrics_{timestamp}.json"

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Results saved to: {output_file}")


if __name__ == "__main__":
    main()
