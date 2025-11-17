"""
Configuration management for TTS Zero-Shot Voice Cloning project.
"""

from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
REFERENCE_DIR = DATA_DIR / "reference"
GENERATED_DIR = DATA_DIR / "generated"
GENERATED_COQUI_DIR = GENERATED_DIR / "coqui"
GENERATED_GPT_SOVITS_DIR = GENERATED_DIR / "gpt_sovits"
GENERATED_TORTOISE_DIR = GENERATED_DIR / "tortoise"

# Results directories
RESULTS_DIR = PROJECT_ROOT / "results"
AUDIO_SAMPLES_DIR = RESULTS_DIR / "audio_samples"
METRICS_FILE = RESULTS_DIR / "metrics_results.json"

# Audio configuration
SAMPLE_RATE = 22050
AUDIO_FORMAT = "wav"

# Model configurations
COQUI_MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"
TORTOISE_PRESET = "fast"  # Options: 'ultra_fast', 'fast', 'standard', 'high_quality'


def ensure_directories():
    """Create all necessary directories if they don't exist."""
    directories = [
        REFERENCE_DIR,
        GENERATED_COQUI_DIR,
        GENERATED_GPT_SOVITS_DIR,
        GENERATED_TORTOISE_DIR,
        AUDIO_SAMPLES_DIR
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
