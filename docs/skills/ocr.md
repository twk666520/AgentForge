
# OCR Skill

Recognise text from images using OCR.

## Installation

```bash
pip install -e core/
pip install -e skills/skill-ocr/
```

Optionally install the OCR backend:

```bash
pip install easyocr
```

## Quick Start

**CLI:**

```bash
python -m ocr_skill.cli photo.png --langs en+ch_sim
```

**Python SDK:**

```python
from ocr_skill import OCREngine

engine = OCREngine({"langs": ["en", "ch_sim"]})
engine.initialize()
result = engine.recognize("photo.png")
print(result.data.raw_text)
engine.cleanup()
```

## API Reference

### OCREngine

Main entry point. Subclasses ``SkillBase``.

**Constructor:**

```python
OCREngine(config: dict | None = None,
          backend: BaseOCRBackend | None = None)
```

- ``config``: Engine configuration.
- ``backend``: Inject a custom backend.

**Config keys:**

| Key | Default | Description |
|-----|---------|-------------|
| backend | easyocr | OCR engine |
| langs | ["en"] | Language codes |
| gpu | False | Use GPU |
| preprocess | {} | Preprocessing options |

**Methods:**

- ``recognize(image) -> SkillResult``
- ``run(image) -> OCRResult``

### Data Models

- ``BBox(x1, y1, x2, y2)`` — Bounding box with ``width``,
  ``height``, ``area``, ``to_dict()``, ``from_list()``.
- ``TextLine(text, bbox, confidence)`` — Single detected line.
- ``OCRResult(lines, ...)`` — Full result with ``raw_text``
  and ``confidence_mean``.

### Image Preprocessing

Functions in ``ocr_skill.preprocess``:

- ``load_image(source)`` — Load from path/bytes/PIL.
- ``to_grayscale(image)`` — Convert to single-channel.
- ``enhance_contrast(image, factor)``
- ``denoise(image, radius)``
- ``sharpen(image, factor)``
- ``standard_pipeline(image, **config)`` — All transforms.
