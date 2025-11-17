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

### 1. Coqui TTS

- **Type**: Open-source TTS library
- **Architecture**: VITS-based models with speaker embeddings
- **Advantages**: Lightweight, well-documented, easy to use
- **Use case**: Fast inference with good quality

### 2. GPT-SoVITS

- **Type**: GPT-based voice cloning
- **Architecture**: Transformer-based acoustic model
- **Advantages**: High-quality voice cloning, good prosody
- **Use case**: High-fidelity voice synthesis

### 3. Tortoise TTS

- **Type**: Autoregressive transformer model
- **Architecture**: GPT-based text-to-speech
- **Advantages**: Very natural-sounding output
- **Use case**: Quality over speed (slower inference)

## Project Structure

```
# Practice 3: Zero-Shot Voice Cloning with TTS Models

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

### 1. Coqui TTS
- **Type**: Open-source TTS library
- **Architecture**: VITS-based models with speaker embeddings
- **Advantages**: Lightweight, well-documented, easy to use
- **Use case**: Fast inference with good quality

### 2. GPT-SoVITS
- **Type**: GPT-based voice cloning
- **Architecture**: Transformer-based acoustic model
- **Advantages**: High-quality voice cloning, good prosody
- **Use case**: High-fidelity voice synthesis

### 3. Tortoise TTS
- **Type**: Autoregressive transformer model
- **Architecture**: GPT-based text-to-speech
- **Advantages**: Very natural-sounding output
- **Use case**: Quality over speed (slower inference)

## Project Structure
```

practica3_tts/
│
├── data/
│   ├── reference/              # Original reference audio
│   │   └── voice_sample.wav
│   └── generated/              # Generated audio outputs
│       ├── coqui/
│       ├── gpt_sovits/
│       └── tortoise/
│
├── models/                     # Model wrapper implementations
│   ├── __init__.py
│   ├── coqui_model.py         # Coqui TTS wrapper
│   ├── gpt_sovits_model.py    # GPT-SoVITS wrapper
│   └── tortoise_model.py      # Tortoise TTS wrapper
│
├── evaluation/                 # Evaluation notebooks and scripts
│   └── evaluation.ipynb       # Metrics calculation and analysis
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── audio_processing.py    # Audio I/O and preprocessing
│   └── config.py              # Configuration management
│
├── scripts/                    # Main execution scripts
│   ├── generate_audio.py      # Generate audio with specified model
│   └── run_all_models.py      # Run all models sequentially
│
├── results/                    # Evaluation results
│   ├── metrics_results.json   # Quantitative metrics
│   └── audio_samples/         # Sample outputs for comparison
│
├── docs/
│   └── memoria.pdf            # Technical report (Spanish)
│
├── Dockerfile                  # Docker image definition
├── Makefile                    # Build and execution recipes
├── requirements.txt            # Python dependencies
├── .dockerignore              # Docker ignore patterns
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

### Generating Audio Samples

Generate audio with Coqui TTS:

```bash
make run-coqui TEXT="Hello, this is a test of voice cloning"
```

Generate audio with GPT-SoVITS:

```bash
make run-gptsovits TEXT="Hello, this is a test of voice cloning"
```

Generate audio with Tortoise TTS:

```bash
make run-tortoise TEXT="Hello, this is a test of voice cloning"
```

Run all models at once:

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
- `make run-coqui` - Run Coqui TTS model
- `make run-gptsovits` - Run GPT-SoVITS model
- `make run-tortoise` - Run Tortoise TTS model
- `make run-all` - Run all models sequentially
- `make jupyter` - Start Jupyter notebook server for evaluation
- `make shell` - Open interactive shell in container
- `make clean` - Clean generated files and cache

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
- **Original Format**: WAV
- **Processing**: Resampled to 22050 Hz if necessary for model compatibility

## Technical Report

A comprehensive technical report (memoria) is included in `docs/memoria.pdf` covering:

- Model selection rationale
- Implementation details and configurations tested
- Quantitative results with at least 2 metrics
- Qualitative analysis and subjective impressions
- Performance comparison (quality, speed, computational requirements)
- Conclusions and recommendations

## License

This project is for academic purposes only. Model licenses:

- **Coqui TTS**: Mozilla Public License 2.0
- **GPT-SoVITS**: MIT License
- **Tortoise TTS**: Apache License 2.0

Reference audio licensed under CC0 (Public Domain) by buggly via Freesound.org.

## Author

**Víctor** - Interactive Intelligent Systems Course
Universidad Intercontinental de la Empresa (UIE)
Practice 3: Zero-Shot Voice Cloning

## Acknowledgments

- Coqui TTS community for the open-source TTS framework
- GPT-SoVITS developers for the voice cloning implementation
- Tortoise TTS team for the high-quality TTS model
- buggly (Freesound.org) for providing the reference audio under CC0 license

---

**Note**: This project implements zero-shot voice cloning without any fine-tuning or model training, focusing on the comparison and evaluation of pre-trained acoustic models. All inference runs on CPU.

```

```

## Requirements

- Docker with GPU support (recommended)
- NVIDIA GPU with CUDA support (optional but recommended)
- At least 8GB of RAM
- ~15GB of disk space for models and dependencies

## Installation & Usage

### Building the Docker Image

```bash
make build
```

### Generating Audio Samples

Generate audio with Coqui TTS:

```bash
make run-coqui TEXT="Hello, this is a test of voice cloning"
```

Generate audio with GPT-SoVITS:

```bash
make run-gptsovits TEXT="Hello, this is a test of voice cloning"
```

Generate audio with Tortoise TTS:

```bash
make run-tortoise TEXT="Hello, this is a test of voice cloning"
```

Run all models at once:

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
- `make run-coqui` - Run Coqui TTS model
- `make run-gptsovits` - Run GPT-SoVITS model
- `make run-tortoise` - Run Tortoise TTS model
- `make run-all` - Run all models sequentially
- `make jupyter` - Start Jupyter notebook server for evaluation
- `make shell` - Open interactive shell in container
- `make clean` - Clean generated files and cache

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
- **Original Format**: WAV
- **Processing**: Resampled to 22050 Hz if necessary for model compatibility

## Technical Report

A comprehensive technical report (memoria) is included in `docs/memoria.pdf` covering:

- Model selection rationale
- Implementation details and configurations tested
- Quantitative results with at least 2 metrics
- Qualitative analysis and subjective impressions
- Performance comparison (quality, speed, computational requirements)
- Conclusions and recommendations

## License

This project is for academic purposes only. Model licenses:

- **Coqui TTS**: Mozilla Public License 2.0
- **GPT-SoVITS**: MIT License
- **Tortoise TTS**: Apache License 2.0

Reference audio licensed under CC0 (Public Domain) by buggly via Freesound.org.

## Author

**Víctor** - Interactive Intelligent Systems Course
Universidad Intercontinental de la Empresa (UIE)
Practice Zero-Shot Voice Cloning

## Acknowledgments

- Coqui TTS community for the open-source TTS framework
- GPT-SoVITS developers for the voice cloning implementation
- Tortoise TTS team for the high-quality TTS model
- buggly (Freesound.org) for providing the reference audio under CC0 license

---

**Note**: This project implements zero-shot voice cloning without any fine-tuning or model training, focusing on the comparison and evaluation of pre-trained acoustic models.
