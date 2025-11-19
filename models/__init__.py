"""
TTS model wrappers for zero-shot voice cloning.
"""

from .yourtts_model import YourTTS
from .xtts_model import XTTS

__all__ = [
    "YourTTS",
    "XTTS",
]
