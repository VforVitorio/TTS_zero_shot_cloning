"""
XTTS v2 model wrapper for zero-shot voice cloning (Coqui TTS).
"""

import numpy as np
from pathlib import Path
from typing import Optional
from TTS.api import TTS

from utils import (
    load_audio,
    save_audio,
    SAMPLE_RATE,
    GENERATED_XTTS_DIR,
    XTTS_MODEL_NAME
)


class XTTS:
    """Wrapper for XTTS v2 model with voice cloning capabilities."""

    def __init__(self):
        """Initialize and load XTTS v2 model."""
        print(f"Loading XTTS v2 model: {XTTS_MODEL_NAME}")
        self.model = TTS(XTTS_MODEL_NAME)
        self.sample_rate = SAMPLE_RATE
        print("XTTS v2 model loaded successfully")

    def _synthesize(self, text: str, reference_audio_path: Path) -> np.ndarray:
        """
        Generate speech using the TTS model with voice cloning.

        Args:
            text: Text to synthesize
            reference_audio_path: Path to reference audio for voice cloning

        Returns:
            Generated audio as numpy array
        """
        # Load reference audio using utils
        reference_audio, _ = load_audio(reference_audio_path)

        # Generate speech with voice cloning
        wav = self.model.tts(
            text=text,
            speaker_wav=str(reference_audio_path),
            language="en"
        )

        # Convert to numpy array if needed
        if not isinstance(wav, np.ndarray):
            wav = np.array(wav)

        return wav

    def generate(
        self,
        text: str,
        reference_audio_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate audio with voice cloning (MAIN FUNCTION).

        Args:
            text: Text to convert to speech
            reference_audio_path: Path to reference audio for voice cloning
            output_path: Optional output path (auto-generated if None)

        Returns:
            Path to generated audio file
        """
        # Generate default output path if not provided
        if output_path is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = GENERATED_XTTS_DIR / f"xtts_{timestamp}.wav"

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Synthesize speech
        print(f"Generating speech with XTTS v2...")
        audio = self._synthesize(text, reference_audio_path)

        # Save audio using utils
        save_audio(audio, output_path, self.sample_rate)
        print(f"Audio saved to: {output_path}")

        return output_path
