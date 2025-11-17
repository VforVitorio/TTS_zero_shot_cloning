"""
TTS model wrappers for zero-shot voice cloning.
"""

from .coqui_model import CoquiTTS
from .gpt_sovits_model import GPTSoVITS

__all__ = [
    "CoquiTTS",
    "GPTSoVITS",
]
