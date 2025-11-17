"""
Audio processing utilities for loading, saving, and preprocessing audio files.
"""

import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Tuple, Optional

from .config import SAMPLE_RATE


def _validate_audio_path(audio_path: Path) -> None:
    """
    Validate that audio file exists.

    Args:
        audio_path: Path to audio file

    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")


def _normalize_audio(audio: np.ndarray) -> np.ndarray:
    """
    Normalize audio to [-1, 1] range.

    Args:
        audio: Audio array

    Returns:
        Normalized audio array
    """
    max_val = np.abs(audio).max()
    if max_val > 0:
        return audio / max_val
    return audio


def load_audio(
    audio_path: Path,
    sample_rate: Optional[int] = None,
    normalize: bool = True
) -> Tuple[np.ndarray, int]:
    """
    Load audio file from disk.

    Args:
        audio_path: Path to audio file
        sample_rate: Target sample rate (uses config default if None)
        normalize: Whether to normalize audio to [-1, 1]

    Returns:
        Tuple of (audio_array, sample_rate)

    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
    _validate_audio_path(audio_path)

    if sample_rate is None:
        sample_rate = SAMPLE_RATE

    # Load audio with librosa
    audio, sr = librosa.load(audio_path, sr=sample_rate, mono=True)

    # Normalize if requested
    if normalize:
        audio = _normalize_audio(audio)

    return audio, sr


def save_audio(
    audio: np.ndarray,
    output_path: Path,
    sample_rate: Optional[int] = None
) -> None:
    """
    Save audio array to disk.

    Args:
        audio: Audio array to save
        output_path: Path where to save audio
        sample_rate: Sample rate (uses config default if None)
    """
    if sample_rate is None:
        sample_rate = SAMPLE_RATE

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save audio file
    sf.write(output_path, audio, sample_rate)


def preprocess_audio(
    audio_path: Path,
    target_sr: Optional[int] = None,
    normalize: bool = True
) -> Tuple[np.ndarray, int]:
    """
    Load and preprocess audio file (load + resample + normalize).

    Args:
        audio_path: Path to audio file
        target_sr: Target sample rate (uses config default if None)
        normalize: Whether to normalize audio

    Returns:
        Tuple of (preprocessed_audio, sample_rate)
    """
    if target_sr is None:
        target_sr = SAMPLE_RATE

    # Load audio
    audio, sr = load_audio(
        audio_path, sample_rate=target_sr, normalize=normalize)

    return audio, sr


def get_audio_duration(audio: np.ndarray, sample_rate: int) -> float:
    """
    Calculate audio duration in seconds.

    Args:
        audio: Audio array
        sample_rate: Sample rate

    Returns:
        Duration in seconds
    """
    return len(audio) / sample_rate


def trim_silence(
    audio: np.ndarray,
    top_db: int = 20
) -> np.ndarray:
    """
    Trim leading and trailing silence from audio.

    Args:
        audio: Audio array
        top_db: Threshold in dB below reference to consider as silence

    Returns:
        Trimmed audio array
    """
    trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return trimmed
