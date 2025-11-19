"""
Utility modules for TTS Zero-Shot Voice Cloning project.
"""

from .config import (
    PROJECT_ROOT,
    REFERENCE_DIR,
    GENERATED_YOURTTS_DIR,
    GENERATED_XTTS_DIR,
    AUDIO_SAMPLES_DIR,
    SAMPLE_RATE,
    YOURTTS_MODEL_NAME,
    XTTS_MODEL_NAME,
    ensure_directories
)

from .audio_processing import (
    load_audio,
    save_audio,
    preprocess_audio,
    get_audio_duration,
    trim_silence
)

__all__ = [
    # Config
    "PROJECT_ROOT",
    "REFERENCE_DIR",
    "GENERATED_YOURTTS_DIR",
    "GENERATED_XTTS_DIR",
    "AUDIO_SAMPLES_DIR",
    "SAMPLE_RATE",
    "YOURTTS_MODEL_NAME",
    "XTTS_MODEL_NAME",
    "ensure_directories",
    # Audio processing
    "load_audio",
    "save_audio",
    "preprocess_audio",
    "get_audio_duration",
    "trim_silence",
]
