"""
Utility modules for TTS Zero-Shot Voice Cloning project.
"""

from .config import (
    PROJECT_ROOT,
    REFERENCE_DIR,
    GENERATED_COQUI_DIR,
    GENERATED_GPT_SOVITS_DIR,
    GENERATED_TORTOISE_DIR,
    AUDIO_SAMPLES_DIR,
    SAMPLE_RATE,
    ensure_directories
)

__all__ = [
    "PROJECT_ROOT",
    "REFERENCE_DIR",
    "GENERATED_COQUI_DIR",
    "GENERATED_GPT_SOVITS_DIR",
    "GENERATED_TORTOISE_DIR",
    "AUDIO_SAMPLES_DIR",
    "SAMPLE_RATE",
    "ensure_directories",
]
