# OCR_pipeline_project

## 1. Short Project Summary
This project runs a two-stage computer vision pipeline to detect product regions in supermarket flyer PDFs and extract text from those regions.
It processes PDF pages rendered as images (intended for flyer-like layouts with product boxes and price text).
The pipeline outputs cropped product images, YOLO label files, and OCR text results from the crops.
It addresses the problem of turning unstructured promotional flyer imagery into machine-readable product-level text signals.
The current implementation is oriented around Tegut flyers and uses a single-page demo flow.

## 2. Technical Overview
**Input data characteristics:**
The main entry point expects a PDF file and renders pages to images using PyMuPDF (fitz).
The demo code processes only the first page of a PDF and assumes a consistent flyer layout.

**Object detection with YOLO:**
The YOLO stage detects product regions on the rendered page image and writes label files plus visualized detection images.
Detections are filtered by confidence, and each box is cropped into per-product images for downstream OCR.

**OCR stage:**
OCR runs on each detected crop using EasyOCR with a German/English character set.
Preprocessing includes grayscale conversion, normalization, and light blurring to stabilize OCR on flyer textures.
A small text cleanup pass normalizes common punctuation/character issues.

**Post-processing and output:**
OCR returns a structured dictionary of full text, line-level text, and confidence metrics.
YOLO crops and labels are stored under per-run output directories, providing traceability from page → detection → crop → OCR.

**Why YOLO precedes OCR:**
The design assumes text of interest is contained within product boxes; using YOLO first reduces background noise and constrains OCR to localized regions.
This approach relies on consistent layout where products and associated text are spatially co-located and detectable by the object detector.

## 3. Folder Structure (Core Section)
```
.
├── src
│   └── portfolio_base
│       ├── app
│       │   ├── app.py
│       │   └── definitions.py
│       ├── tegut_ocr
│       │   ├── ocr_easy.py
│       │   ├── yolo_detect.py
│       │   └── paths.py
│       ├── models
│       │   └── tegut_yolo.pt
│       └── data
│           ├── input
│           │   └── pdf_new
│           │       └── *.pdf
│           └── output
│               └── runs
│                   └── run_*/ 
│                       ├── pages
│                       ├── yolo
│                       └── crops
├── requirements.txt
└── runtime.txt
```

**Folder responsibilities and data flow**
- **`.devcontainer/`**: Development container configuration used for local or cloud-based environments.
- **`.idea/`**: IDE metadata (not part of the pipeline logic).
- **`.venv/`**: Local Python virtual environment with third-party packages.
- **`src/`**: Application source code and model/data assets.
  - **`src/portfolio_base/app/`**: Streamlit UI and helper utilities; orchestrates the demo flow and exposes pipeline steps.
  - **`src/portfolio_base/tegut_ocr/`**: Core computer vision + OCR logic (YOLO detection, OCR extraction, and path configuration).
  - **`src/portfolio_base/models/`**: YOLO model weights used for detection.
  - **`src/portfolio_base/data/`**: Input PDFs, output pages, YOLO labels, crops, and run artifacts.
- **`requirements.txt`, `runtime.txt`**: Runtime and dependency metadata.

**Data flow between folders**
1. **Detection**: `src/portfolio_base/tegut_ocr/yolo_detect.py` reads PDFs and writes page images into `src/portfolio_base/data/output/.../pages`.
2. **Cropping**: YOLO detections are saved under `src/portfolio_base/data/output/.../yolo`, and crops are written to `src/portfolio_base/data/output/.../crops/{raw,ocr}`.
3. **OCR**: `src/portfolio_base/tegut_ocr/ocr_easy.py` consumes crops and returns structured OCR results used by the Streamlit app.
4. **Postprocessing/Export**: `src/portfolio_base/app/definitions.py` includes helpers for masking, zipping, and MakeSense export/import of labels.

**Where key logic lives**
- **Computer vision logic**: `src/portfolio_base/tegut_ocr/yolo_detect.py` (PDF rendering, YOLO inference, crop extraction).
- **OCR logic**: `src/portfolio_base/tegut_ocr/ocr_easy.py` (EasyOCR reader + preprocessing + cleanup).
- **Data preprocessing**: `src/portfolio_base/tegut_ocr/ocr_easy.py` and `src/portfolio_base/app/definitions.py` (OCR masking and normalization helpers).
- **Pipeline orchestration**: `src/portfolio_base/app/app.py` (Streamlit-based flow and UI-driven execution).
- **Configuration/model weights**: `src/portfolio_base/tegut_ocr/paths.py` and `src/portfolio_base/models/tegut_yolo.pt`.

## 4. Engineering & Design Decisions
The project uses a two-stage pipeline (YOLO → OCR) to isolate product regions before text extraction.
This reduces OCR noise compared to full-page OCR and aligns with flyer layouts where text is typically embedded within product boxes.
Modularity is achieved by separating detection, OCR, and app orchestration into distinct modules and folders.
The pipeline can be extended by swapping YOLO weights, adding new detectors, or integrating alternative OCR engines.

**Limitations and failure modes**
- The demo processes only the first page of a PDF, which limits multi-page flyer coverage.
- Detection quality depends on the Tegut-specific YOLO model and may degrade on other layouts or seasons.
- OCR errors are likely for low-resolution images, heavy compression artifacts, or stylized fonts.
- The pipeline assumes that product text is visually near or inside the detected product region; mismatches can yield incomplete OCR.

## 5. What This Project Demonstrates
This project demonstrates object detection and OCR integration in a multi-stage vision pipeline.
It shows practical handling of unstructured flyer imagery, conversion from PDFs to images, and structured text extraction from crops.
The codebase is relevant to roles focused on computer vision, OCR systems, ML model deployment, and end-to-end pipeline engineering.
