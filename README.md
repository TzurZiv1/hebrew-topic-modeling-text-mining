# Hebrew Topic Modeling (Text Mining)

This project collects Hebrew text from Wikipedia and UGC (Emotion UGC from HeBERT),
preprocesses it, and runs several topic modeling baselines and advanced models
(LDA/LSA/NMF, Top2Vec, CTM, Contextual-Top2Vec). The notebooks contain saved
outputs from prior runs (Colab/Kaggle) so you can review results without rerunning.

## Project layout
- `notebooks/` - stage-by-stage notebooks (data -> preprocessing -> models -> comparison).
- `results_artifacts/` - metrics, topics, and example documents exported from notebooks.
- `report/` - final report PDF goes here.
- `scripts/run_pipeline.py` - end-to-end runner for notebook execution.
- `project_paths.py` - shared path configuration helper.

## Local data (current repo)
If you already have data in `data/`, you can skip Stage 1/2 and start from Stage 3.
Expected files for the later stages:
- `data/processed_wiki.parquet`
- `data/processed_ugc.parquet`

Optional raw/intermediate inputs for Stage 1/2:
- `data/wiki_25k_truncated.parquet`
- `data/hebert_ugc_ready.parquet`

## Data sources (dataset description)
Sources:
- UGC: Emotion UGC dataset from the HeBERT GitHub `data.zip`.
- Wiki: Hebrew Wikipedia dump from `hewiki-latest-pages-articles.xml.bz2`.

Licensing & privacy:
- Wikipedia content is CC BY-SA; keep attribution if redistributing derived data.
- The HeBERT UGC dataset license is defined in its source repo; review it before sharing.
- Avoid storing personally identifiable information in artifacts or reports.

Collection time:
- Wikipedia data is pulled from the latest dump at download time.
- HeBERT data is used as published in the repository (original collection date is
  not specified in the dataset repo, so the release snapshot is used).

Limitations and coverage:
- Wikipedia text is encyclopedic and editor-written; it does not represent casual
  language or all social groups.
- UGC is noisy (slang, typos, short comments) and reflects only users who choose
  to comment, which can bias topics.
- Some stages truncate articles (e.g., first 100 words) to reduce memory usage,
  which may reduce context and coherence.

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Path configuration
By default, paths resolve to the repo root. You can override with env vars:
- `HTM_ROOT` or `HTM_BASE_DIR`
- `HTM_DATA_DIR`
- `HTM_MODELS_DIR`
- `HTM_RESULTS_DIR`

PowerShell example:
```powershell
$env:HTM_ROOT = "C:\path\to\hebrew-topic-modeling-text-mining"
```

## End-to-end run (notebooks)
This script runs notebooks in order (dry-run by default).

```bash
python scripts/run_pipeline.py --execute --from-stage 1 --to-stage 5
```

Common options:
- `--skip-top2vec` if no GPU.
- `--data-root`, `--models-root`, `--results-root` to point to external storage.

## Notebook order
1. `notebooks/hebrew_topic_stage1_datasets_prep final.ipynb`
2. `notebooks/hebrew_topic_stage2_preprocessing final.ipynb`
3. `notebooks/hebrew_topic_stage3_baselines_cpu final.ipynb`
4. `notebooks/hebrew_topic_stage3_top2vec_gpu final.ipynb`
5. `notebooks/hebrew_topic_stage-4-advanced-topic-models-final.ipynb`
6. `notebooks/hebrew_topic_stage5_comparison_notebook_fixed.ipynb`

## Modeling notes
Topic modeling is unsupervised, so there is no train/validation/test split.
Instead, the notebooks compare multiple K values and models using coherence,
topic diversity, and qualitative inspection.

## Outputs
Artifacts are exported to `results_artifacts/`:
- `metrics_*.csv` - model-level metrics (coherence/diversity).
- `topics_*.csv` - top terms per topic.
- `examples_*.csv` - example documents per topic.

## Report
Place the final PDF report in `report/` to satisfy the submission requirement.
