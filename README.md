# Zero-Shot Voice Cloning with TTS Models

## Overview

This project implements and compares different Text-to-Speech (TTS) acoustic models for zero-shot voice cloning. Zero-shot voice cloning allows mimicking a person's voice from just a few seconds of audio, without requiring expensive training or fine-tuning of the model.

The system takes a short reference audio sample and generates synthetic speech saying completely different words, attempting to match the characteristics of the original voice.

## Objectives

- Implement at least 2 different TTS acoustic models with zero-shot voice cloning capabilities
- Generate synthetic audio samples from a reference voice
- Evaluate model performance using both objective metrics and subjective assessment
- Compare models based on voice similarity, audio quality, and inference latency
- Document implementation decisions and analyze results in a technical report

## Models Implemented

This project implements **3 different Coqui TTS models** for comparison:

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

### 3. VITS

- **Type**: Variational Inference TTS
- **Architecture**: End-to-end VITS model
- **Model**: `tts_models/en/vctk/vits`
- **Advantages**: Lightweight, fast inference
- **Use case**: Fast generation with decent quality
- **⚠️ SYSTEM REQUIREMENT**: Requires `espeak-ng` (included in Dockerfile)

## Important License Information

### XTTS v2 License (CPML)

**XTTS v2 requires accepting Coqui's CPML (Coqui Public Model License) terms.**

This project automatically accepts the **non-commercial license** by setting the `COQUI_TOS_AGREED` environment variable in the code. This is necessary because XTTS v2 normally requires interactive license acceptance, which doesn't work in Docker containers.

**License details:**
- **Non-commercial use**: Covered by CPML license (https://coqui.ai/cpml) - **automatically accepted by this project**
- **Commercial use**: Requires purchasing a commercial license from Coqui (licensing@coqui.ai)

**Why this is needed:**
When running XTTS v2 in Docker without TTY, the model tries to ask for license confirmation interactively, causing an "EOF when reading a line" error. Our implementation bypasses this by programmatically accepting the non-commercial terms.

**Implementation location:**
- File: `models/xtts_model.py`
- Line: `os.environ['COQUI_TOS_AGREED'] = '1'`

If you need commercial use, you must:
1. Purchase a license from licensing@coqui.ai
2. Remove or modify the automatic acceptance in the code
3. Follow Coqui's commercial licensing terms

## System Requirements

### VITS Model - espeak-ng Dependency

The VITS model requires **espeak-ng** for text phonemization (converting text to phonemes).

**Why this is needed:**
VITS uses phoneme-based synthesis, which requires a phonemization backend. Without `espeak-ng`, you'll get the error:
```
[!] No espeak backend found. Install espeak-ng or espeak to your system.
```

**Solution:**
The Dockerfile automatically installs `espeak-ng` as part of the system dependencies. No manual action required.

**Implementation location:**
- File: `Dockerfile`
- Line: `espeak-ng \` in the apt-get install command

## Project Structure

```
TTS_zero_shot_cloning/
│
├── data/
│   ├── reference/              # Original reference audio
│   │   └── .gitkeep
│   └── generated/              # Generated audio outputs
│       ├── yourtts/            # YourTTS generated audio
│       ├── xtts/               # XTTS v2 generated audio
│       └── vits/               # VITS generated audio
│
├── models/                     # Model wrapper implementations
│   ├── __init__.py
│   ├── yourtts_model.py        # YourTTS wrapper
│   ├── xtts_model.py           # XTTS v2 wrapper (with license handling)
│   └── vits_model.py           # VITS wrapper
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
│   ├── generate_vits.py        # Generate with VITS
│   └── run_all.py              # Run all models sequentially
│
├── results/                    # Evaluation results
│   ├── metrics_results.json    # Quantitative metrics
│   └── audio_samples/          # Sample outputs for comparison
│
├── docs/
│   └── memoria.pdf             # Technical report (Spanish)
│
├── Dockerfile                  # Docker image definition (includes espeak-ng)
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
- Install system dependencies (ffmpeg, espeak-ng, etc.)
- Install Python dependencies
- Set up the environment for all 3 models

### Generating Audio Samples

Generate audio with YourTTS:

```bash
make run-yourtts TEXT="Hello, this is a test of voice cloning"
```

Generate audio with XTTS v2:

```bash
make run-xtts TEXT="Hello, this is a test of voice cloning"
```

Generate audio with VITS:

```bash
make run-vits TEXT="Hello, this is a test of voice cloning"
```

Run all models at once and compare:

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
- `make run-vits` - Run VITS model
- `make run-all` - Run all models sequentially and compare results
- `make jupyter` - Start Jupyter notebook server for evaluation
- `make shell` - Open interactive shell in container
- `make clean` - Remove Docker image

## Evaluation Metrics

Este proyecto evalúa los modelos TTS usando 3 métricas objetivas principales:

### 1. Speaker Similarity (Similitud del Hablante) ⭐ PRINCIPAL

Mide qué tan similar suena la voz generada respecto a la voz de referencia.

**Herramientas:**
- **Resemblyzer**: Extrae embeddings de voz usando GE2E (Generalized End-to-End)
- **SpeechBrain ECAPA-TDNN**: Speaker verification embeddings de alta precisión

**Métrica:** Cosine similarity entre embeddings del audio de referencia vs audio generado

**Rango:** 0-1 (más cercano a 1 = mayor similitud de voz)

**Interpretación:**
- `>0.8`: Excelente similitud
- `0.6-0.8`: Buena similitud
- `<0.6`: Similitud pobre

### 2. Audio Quality (Calidad de Audio)

Evalúa la calidad perceptual y técnica del audio generado.

**Herramientas:**
- **PESQ** (Perceptual Evaluation of Speech Quality): Calidad perceptual de voz
- **STOI** (Short-Time Objective Intelligibility): Inteligibilidad del habla

**Rango PESQ:** -0.5 a 4.5 (más alto = mejor calidad)
**Rango STOI:** 0-1 (más alto = mayor inteligibilidad)

**Métricas adicionales:**
- Signal-to-Noise Ratio (SNR)
- Análisis espectral

### 3. Inference Time (Tiempo de Inferencia)

Mide la velocidad de generación del modelo.

**Métrica:** Tiempo de generación por segundo de audio (RTF - Real-Time Factor)

**Cálculo:** `RTF = tiempo_generación / duración_audio`

**Interpretación:**
- `RTF < 1`: Más rápido que tiempo real (ideal)
- `RTF = 1`: Tiempo real
- `RTF > 1`: Más lento que tiempo real

**Ejemplo:** RTF = 0.5 significa que genera 1 segundo de audio en 0.5 segundos

---

### Evaluación Subjetiva (Opcional)

- **MOS** (Mean Opinion Score): Evaluación humana de naturalidad (escala 1-5)
- **Prosody**: Entonación, ritmo y patrones de énfasis

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

## Technical Report

A comprehensive technical report (memoria) is included in `docs/memoria.pdf` covering:

- Model selection rationale
- Implementation details and configurations tested
- Quantitative results with at least 2 metrics
- Qualitative analysis and subjective impressions
- Performance comparison (quality, speed, computational requirements)
- Conclusions and recommendations

## Troubleshooting

### XTTS v2: "EOF when reading a line" error

**Cause:** XTTS v2 requires accepting license terms interactively, which fails in Docker.

**Solution:** The code automatically accepts the non-commercial CPML license by setting `COQUI_TOS_AGREED=1`. This is implemented in `models/xtts_model.py`.

If you see this error, verify that the environment variable is being set correctly in the model initialization.

### VITS: "No espeak backend found" error

**Cause:** VITS requires `espeak-ng` for phonemization.

**Solution:** Rebuild the Docker image with `make build`. The Dockerfile includes `espeak-ng` installation.

If the error persists, verify that `espeak-ng` is in the Dockerfile's apt-get install list.

## License

This project is for academic purposes only.

**Model licenses:**
- **YourTTS**: Mozilla Public License 2.0 (Coqui TTS)
- **XTTS v2**: Coqui Public Model License (CPML) - Non-commercial use only
  - Commercial use requires purchasing a license from licensing@coqui.ai
  - This project automatically accepts non-commercial terms
- **VITS**: Mozilla Public License 2.0 (Coqui TTS)

**Reference audio:** Licensed under CC0 (Public Domain) by buggly via Freesound.org.

## Author

**Víctor** - Interactive Intelligent Systems Course
Universidad Intercontinental de la Empresa (UIE)
Practice 3: Zero-Shot Voice Cloning

## Acknowledgments

- Coqui TTS community for the open-source TTS framework
- Coqui AI team for developing YourTTS, XTTS v2, and VITS models
- buggly (Freesound.org) for providing the reference audio under CC0 license
- espeak-ng developers for the phonemization backend

---

**Note**: This project implements zero-shot voice cloning without any fine-tuning or model training, focusing on the comparison and evaluation of pre-trained acoustic models. All inference runs on CPU.
