# Zero-Shot Voice Cloning with TTS Models

## Overview

This project implements and compares different Text-to-Speech (TTS) acoustic models for zero-shot voice cloning. Zero-shot voice cloning allows mimicking a person's voice from just a few seconds of audio, without requiring expensive training or fine-tuning of the model.

The system takes a short reference audio sample and generates synthetic speech saying completely different words, attempting to match the characteristics of the original voice.

## Phrases for Evaluation

The following phrases are used for testing and comparing the TTS models. Each phrase is designed to test different aspects of speech synthesis including varied topics, natural prosody, and sentence complexity.

**Phrase 1 - Technology & Lifestyle:**

```
Technology has changed the way we live. From smartphones to smart homes, everything is connected. On a rainy afternoon, there's nothing better than curling up with a good book and a cup of hot chocolate. The importance of healthy eating cannot be overstated. A balanced diet fuels our bodies and helps us stay strong. Traveling to a new country opens your mind. You meet different people, taste new food, and learn about their culture.
```

**Phrase 2 - Music & Emotions:**

```
Music has the power to transport us to different times and places. A single melody can evoke memories we thought were forgotten. Scientists believe that listening to music reduces stress and improves our mental health. Whether it's classical, jazz, or pop, every genre has its unique way of touching our souls.
```

**Phrase 3 - Environment & Ocean:**

```
The ocean covers more than seventy percent of our planet's surface. It's home to countless species, from tiny plankton to massive whales. Climate change is affecting marine ecosystems in unprecedented ways. We must act now to protect these vital waters for future generations.
```

**Phrase 4 - Learning & Growth:**

```
Learning a new skill requires patience and dedication. At first, progress may seem slow and frustrating. But with consistent practice, improvement becomes visible. The journey of mastering something new teaches us valuable lessons about perseverance and self-belief.
```

## Objectives

- Implement at least 2 different TTS acoustic models with zero-shot voice cloning capabilities
- Generate synthetic audio samples from a reference voice
- Evaluate model performance using both objective metrics and subjective assessment
- Compare models based on voice similarity, audio quality, and inference latency
- Document implementation decisions and analyze results in a technical report

## Models Implemented

This project implements **2 different Coqui TTS models** for comparison:

### 1. YourTTS

- **Type**: Multilingual multi-speaker TTS model
- **Architecture**: VITS-based with speaker encoder
- **Model**: `tts_models/multilingual/multi-dataset/your_tts`
- **Advantages**: Good balance of quality and speed, supports multiple languages
- **Use case**: General-purpose zero-shot voice cloning

### 2. XTTS v2

- **Type**: Advanced multilingual TTS with zero-shot capabilities
- **Architecture**: Enhanced VITS with cross-lingual features
- **Model**: `tts_models/multilingual/multi-dataset/xtts_v2`
- **Advantages**: High-quality voice cloning, excellent prosody
- **Use case**: High-fidelity voice synthesis
- **⚠️ LICENSE REQUIREMENT**: See section below

## Project Structure

```
TTS_zero_shot_cloning/
│
├── data/
│   ├── reference/              # Original reference audio
│   │   └── .gitkeep
│   └── generated/              # Generated audio outputs
│       ├── yourtts/            # YourTTS generated audio
│       └── xtts/               # XTTS v2 generated audio
│
├── models/                     # Model wrapper implementations
│   ├── __init__.py
│   ├── yourtts_model.py        # YourTTS wrapper
│   └── xtts_model.py           # XTTS v2 wrapper (with license handling)
│
├── evaluation/                 # Evaluation notebooks and scripts
│   └── evaluation.ipynb        # Metrics calculation and analysis
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── audio_processing.py     # Audio I/O and preprocessing
│   └── config.py               # Configuration management
│
├── scripts/                    # Main execution scripts
│   ├── generate_yourtts.py     # Generate with YourTTS
│   ├── generate_xtts.py        # Generate with XTTS v2
│   └── run_all.py              # Run all models sequentially
│
├── results/                    # Evaluation results
│   ├── metrics_results.json    # Quantitative metrics
│   └── audio_samples/          # Sample outputs for comparison
│
├── docs/
│   └── memoria.pdf             # Technical report (Spanish)
│
├── Dockerfile                  # Docker image definition
├── Makefile                    # Build and execution recipes
├── requirements.txt            # Python dependencies
├── .dockerignore               # Docker ignore patterns
└── README.md                   # This file
```

## Requirements

- Docker (CPU-only, no GPU required)
- At least 8GB of RAM
- ~10GB of disk space for models and dependencies
- Multi-core CPU recommended for faster inference

**Note**: This project runs entirely on CPU. While GPU acceleration is optional, CPU inference is sufficient for TTS models and may even be faster for some smaller models.

## Installation & Usage

### Building the Docker Image

```bash
make build
```

This will:

- Install system dependencies (ffmpeg, etc.)
- Install Python dependencies
- Set up the environment for both models

### Generating Audio Samples

Generate audio with YourTTS:

```bash
make run-yourtts TEXT="Hello, this is a test of voice cloning"
```

Generate audio with XTTS v2:

```bash
make run-xtts TEXT="Hello, this is a test of voice cloning"
```

Run both models at once and compare:

```bash
make run-all TEXT="Hello, this is a test of voice cloning"
```

### Evaluation

Open the evaluation notebook:

```bash
make jupyter
```

Then navigate to `evaluation/evaluation.ipynb` in your browser.

### Available Make Commands

- `make build` - Build Docker image
- `make run-yourtts` - Run YourTTS model
- `make run-xtts` - Run XTTS v2 model
- `make run-all` - Run both models sequentially and compare results
- `make jupyter` - Start Jupyter notebook server for evaluation
- `make shell` - Open interactive shell in container
- `make clean` - Remove Docker image

## Evaluation Metrics

This project evaluates TTS models using 3 main objective metrics:

### 1. Speaker Similarity ⭐ PRIMARY

Measures how similar the generated voice sounds compared to the reference voice.

**Tools:**

- **Resemblyzer**: Extracts voice embeddings using GE2E (Generalized End-to-End)
- **SpeechBrain ECAPA-TDNN**: High-precision speaker verification embeddings

**Metric:** Cosine similarity between reference audio embeddings vs generated audio

**Range:** 0-1 (closer to 1 = higher voice similarity)

**Interpretation:**

- `>0.8`: Excellent similarity
- `0.6-0.8`: Good similarity
- `<0.6`: Poor similarity

### 2. Audio Quality

Evaluates the perceptual and technical quality of generated audio.

**Tools:**

- **PESQ** (Perceptual Evaluation of Speech Quality): Perceptual voice quality
- **STOI** (Short-Time Objective Intelligibility): Speech intelligibility

**PESQ Range:** -0.5 to 4.5 (higher = better quality)
**STOI Range:** 0-1 (higher = better intelligibility)

**Additional Metrics:**

- Signal-to-Noise Ratio (SNR)
- Spectral analysis

### 3. Inference Time

Measures the model's generation speed.

**Metric:** Generation time per second of audio (RTF - Real-Time Factor)

**Calculation:** `RTF = generation_time / audio_duration`

**Interpretation:**

- `RTF < 1`: Faster than real-time (ideal)
- `RTF = 1`: Real-time
- `RTF > 1`: Slower than real-time

**Example:** RTF = 0.5 means it generates 1 second of audio in 0.5 seconds

---

### Subjective Evaluation (Optional)

- **MOS** (Mean Opinion Score): Human evaluation of naturalness (scale 1-5)
- **Prosody**: Intonation, rhythm, and emphasis patterns

## Reference Audio

The reference audio used in this project is:

- **Source**: Freesound.org
- **Audio URL**: https://freesound.org/people/buggly/sounds/752370/
- **Author**: buggly
- **License**: Creative Commons 0 (CC0 - Public Domain)
- **Description**: Male voice sample suitable for TTS voice cloning
- **Language**: English
- **Original Format**: WAV/MP3 (both supported)
- **Processing**: Resampled to 22050 Hz if necessary for model compatibility

**Note**: This project implements zero-shot voice cloning without any fine-tuning or model training, focusing on the comparison and evaluation of pre-trained acoustic models. All inference runs on CPU.
