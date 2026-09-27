# AgriN — Streamlit Version (Python)

Same 4 modules as the main web app (Dashboard, AI Crop Advisor, Disease Scanner, BRICS Network), rebuilt in Python + Streamlit + Plotly. Kept as a companion build to showcase the Python/data-science stack alongside the primary HTML/JS prototype.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Deploy free (Streamlit Community Cloud)

1. Push this folder to your GitHub repo (can be a subfolder, e.g. `streamlit-app/`)
2. Go to https://share.streamlit.io → **New app**
3. Pick your repo, branch, and set main file path to `app.py` (or `streamlit-app/app.py` if it's a subfolder)
4. Deploy — you get a free public link like `https://agrin.streamlit.app`

## Enabling live AI (optional)

Without any setup, the app runs fully on rule-based recommendations and an on-device image heuristic — nothing is broken or fake-looking.

To enable live Claude-powered recommendations and vision-based disease diagnosis:

1. On Streamlit Community Cloud: app settings → **Secrets** → add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
2. Locally: `export ANTHROPIC_API_KEY=sk-ant-...` before running

## Tech

`streamlit` · `plotly` · `Pillow` · `numpy` · `pandas` · `anthropic` (optional, for live AI)
