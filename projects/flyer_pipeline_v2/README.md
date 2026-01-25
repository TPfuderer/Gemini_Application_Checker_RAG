# Flyer Pipeline v2 — Web Scraping Only

## 1. Short Project Summary

The **web scraping pipeline** in `flyer_pipeline_v2` collects weekly retail flyer offers from multiple grocery chains (e.g., Edeka, Netto, Rewe, Kaufland, Tegut, Lidl) and exports structured CSVs plus offer images into a run-specific output folder. It solves the problem of automating flyer data acquisition from heterogeneous retailer websites and produces a repeatable, weekly ETL-style dataset (scrape → validate → deduplicate/merge). The primary output is a per-shop CSV (with product, pricing, and image path fields) alongside downloaded images organized under each run’s directory. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L14-L101】【F:flyer_pipeline_v2/web_scraping/utils/paths.py†L6-L34】【F:flyer_pipeline_v2/web_scraping/scrapers/edeka/scrape_edeka.py†L25-L132】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/scrape_kaufland.py†L18-L206】

## 2. Technical Overview

### Target websites & assumptions
- The pipeline targets retailer offer pages (Edeka, Netto, Rewe, Kaufland, Tegut, Lidl) and assumes those pages expose product tiles and images in the rendered DOM that can be accessed via Playwright and standard DOM selectors. It also assumes weekly runs, encoded as `YYYY_KWXX`, are appropriate for organizing output snapshots. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L14-L59】【F:flyer_pipeline_v2/web_scraping/utils/paths.py†L13-L34】

### Scraping strategy
- Each shop has its own scraper module under `web_scraping/scrapers/<shop>/`, using Playwright to load pages, scroll/load dynamic content, extract product data, and download images via `requests`. Examples include:
  - **Edeka**: scrolls the offer page, parses product cards, and saves images/CSV. 【F:flyer_pipeline_v2/web_scraping/scrapers/edeka/scrape_edeka.py†L36-L132】
  - **Kaufland**: scrolls, clicks “show more,” collects product tiles, and exports images/CSV. 【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/scrape_kaufland.py†L38-L206】
  - **Rewe**: scrolls the offer page, extracts products, and stores images/CSV for each market. 【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/scrape_rewe.py†L38-L178】
- A helper (`utils/kaufda_finder.py`) exists for finding Kaufda flyer viewer links using Playwright, which can be reused when a shop’s content is embedded in Kaufda. 【F:flyer_pipeline_v2/web_scraping/utils/kaufda_finder.py†L1-L75】

### Error handling & retries
- `run_all.py` orchestrates scrapers shop-by-shop, writes state to `state.json`, and continues across failures by marking a shop as `failed` while proceeding to the next. This makes the run resilient to individual site errors or page changes. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L62-L120】
- Validation is “soft”: `postprocess.validate.validate_shop_output` emits warnings for missing files/columns but does not raise errors, preventing the pipeline from stopping due to partial outputs. 【F:flyer_pipeline_v2/postprocess/validate.py†L10-L71】

### Output format & storage
- Output is stored under `web_scraping/runs/<YYYY_KWXX>/<shop>/` and includes `<shop>_<run>.csv` and `images_<shop>/` for associated product images. Paths are constructed via `utils/paths.py` for portability. 【F:flyer_pipeline_v2/web_scraping/utils/paths.py†L6-L34】
- CSVs include fields such as product name, price, optional base price/unit, validity dates, and image path references. This is consistent across scrapers (e.g., Edeka, Kaufland, Rewe). 【F:flyer_pipeline_v2/web_scraping/scrapers/edeka/scrape_edeka.py†L94-L132】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/scrape_kaufland.py†L130-L187】【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/scrape_rewe.py†L121-L176】

### Deduplication & normalization
- **Kaufland**: a dedicated dedup step normalizes product names, drops duplicates, and cleans unused images. 【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/deduplicate.py†L24-L82】
- **Rewe**: a merge step combines multiple market-specific CSVs, deduplicates by normalized product name + price, consolidates images, and writes a final CSV. 【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/merge.py†L11-L112】

## 3. Folder Structure (Core Section)

Below is the **`flyer_pipeline_v2` tree only**, excluding bulky or non-core artifacts like images, model binaries, or CSVs. Treat this tree as the RAG index for the pipeline’s web scraping logic.

```
flyer_pipeline_v2/
├── README.md
├── flyer_ocr/
│   ├── pipeline/
│   │   ├── step_1_yolo.py
│   │   ├── step_2_makesense_export.py
│   │   ├── step_3_makesense_import.py
│   │   ├── step_4_matching.py
│   │   ├── step_5_cropper.py
│   │   ├── step_6_clean.py
│   │   ├── step_7_product_extract.py
│   │   └── step_8_remerge.py
│   └── utils/
│       └── paths.py
├── postprocess/
│   ├── __init__.py
│   └── validate.py
└── web_scraping/
    ├── __init__.py
    ├── run_all.py
    ├── test_pipeline.py
    ├── utils/
    │   ├── __init__.py
    │   ├── kaufda_finder.py
    │   └── paths.py
    └── scrapers/
        ├── __init__.py
        ├── aldi/
        │   ├── __init__.py
        │   ├── scrape_aldi.py
        │   └── scrape_aldi_from_homepage.py
        ├── dm/
        │   └── __init__.py
        ├── edeka/
        │   ├── __init__.py
        │   ├── scrape_edeka.py
        │   └── tst.py
        ├── kaufland/
        │   ├── __init__.py
        │   ├── deduplicate.py
        │   └── scrape_kaufland.py
        ├── lidl/
        │   ├── __init__.py
        │   └── scrape_lidl.py
        ├── müller/
        │   └── __init__.py
        ├── netto/
        │   ├── __init__.py
        │   └── scrape_netto.py
        ├── penny/
        │   └── __init__.py
        ├── rewe/
        │   ├── __init__.py
        │   ├── merge.py
        │   └── scrape_rewe.py
        ├── rossmann/
        │   └── __init__.py
        └── tegut/
            ├── __init__.py
            └── scrape_tegut.py
```

### What runs, and in what order
1. **`web_scraping/run_all.py`** is the orchestrator. It computes the weekly run tag, creates a run folder, executes each scraper in its `SHOPS` list, validates output, and triggers dedup/merge steps where applicable. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L14-L120】
2. **`web_scraping/scrapers/<shop>/scrape_*.py`** runs shop-specific scraping with Playwright and writes `CSV + images` into the run folder. 【F:flyer_pipeline_v2/web_scraping/scrapers/edeka/scrape_edeka.py†L25-L132】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/scrape_kaufland.py†L18-L206】【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/scrape_rewe.py†L38-L189】
3. **`postprocess/validate.py`** performs a soft validation pass (warnings only) to highlight schema/quality issues without stopping the pipeline. 【F:flyer_pipeline_v2/postprocess/validate.py†L10-L71】
4. **Dedup/Merge** (if configured):
   - **Kaufland**: `deduplicate.py` normalizes product names, drops duplicates, and prunes unused images. 【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/deduplicate.py†L24-L82】
   - **Rewe**: `merge.py` consolidates market outputs and deduplicates by normalized product + price. 【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/merge.py†L11-L112】

### Data flow (end-to-end)
```
Retailer pages → Playwright scrapers → runs/YYYY_KWXX/<shop>/{csv + images}
                              ↘ validate.py (warnings only)
                              ↘ deduplicate.py / merge.py (shop-specific)
```
This flow is implemented by the shop scrapers, `run_all.py`, and the postprocess utilities. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L14-L120】【F:flyer_pipeline_v2/postprocess/validate.py†L10-L71】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/deduplicate.py†L24-L82】【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/merge.py†L11-L112】

## 4. Engineering & Design Decisions

- **Playwright-first scraping**: Retailer sites are dynamic; using Playwright enables DOM rendering, scrolling, and click-based loading of offers that static HTTP requests would miss. 【F:flyer_pipeline_v2/web_scraping/scrapers/edeka/scrape_edeka.py†L42-L83】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/scrape_kaufland.py†L45-L106】
- **Weekly run tags**: Runs are grouped by ISO week (`YYYY_KWXX`) to produce clean, repeatable snapshots and make incremental comparisons straightforward. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L29-L59】【F:flyer_pipeline_v2/web_scraping/utils/paths.py†L13-L34】
- **Robustness vs. speed trade-off**: Each scraper loads pages, scrolls to ensure content is visible, and downloads images; this is slower than headless HTML parsing but more resilient to JS-heavy sites. 【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/scrape_rewe.py†L70-L108】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/scrape_kaufland.py†L65-L106】
- **Soft validation**: Validation emits warnings but does not halt the run. This favors pipeline continuity even when a single shop’s output is imperfect. 【F:flyer_pipeline_v2/postprocess/validate.py†L10-L71】
- **Limitations**: Scrapers rely on site-specific selectors and scroll logic; significant DOM changes or anti-bot measures can break extraction until selectors are updated. The pipeline therefore favors transparency and recoverability (state tracking, warnings) over strict failure. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L62-L120】【F:flyer_pipeline_v2/web_scraping/scrapers/edeka/scrape_edeka.py†L42-L83】

## 5. What This Project Demonstrates

- **Data engineering skill**: structured extraction into normalized CSV outputs with clear storage conventions and post-processing steps (validation, dedup/merge). 【F:flyer_pipeline_v2/web_scraping/utils/paths.py†L6-L34】【F:flyer_pipeline_v2/web_scraping/scrapers/kaufland/deduplicate.py†L24-L82】【F:flyer_pipeline_v2/web_scraping/scrapers/rewe/merge.py†L11-L112】
- **Automation reliability**: state tracking and soft validation allow partial successes to persist and reduce manual restarts. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L62-L120】【F:flyer_pipeline_v2/postprocess/validate.py†L10-L71】
- **Pipeline design**: the web scraping folder is runnable in isolation (`run_all.py`) and uses local relative path utilities to keep outputs self-contained under `web_scraping/runs`. 【F:flyer_pipeline_v2/web_scraping/run_all.py†L14-L120】【F:flyer_pipeline_v2/web_scraping/utils/paths.py†L6-L34】
