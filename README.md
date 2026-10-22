# CO2 Emissions Prediction – Deployment Guide

Files: `CO2_Emissions_10fold_CV.ipynb`, `CO2_Emissions_Canada.csv`, `co2_model.pkl`, `app.py`, `requirements.txt`

## Deploy on Streamlit Community Cloud (free)
1. Create a GitHub account/repo (e.g. `co2-emissions-app`, public).
2. Upload `app.py`, `requirements.txt`, `co2_model.pkl` (and the csv/notebook) to the repo root.
3. Go to https://share.streamlit.io, sign in with GitHub, click **Create app**,
   choose the repo, branch `main`, main file `app.py`, then **Deploy**.
4. Copy the live URL (https://....streamlit.app) and paste it at the very top of the notebook.
5. Submit to Google Classroom: notebook (with link), dataset, `co2_model.pkl`. Deadline: Sun 25 Oct 2026, 23:59.

Local test: `pip install -r requirements.txt && streamlit run app.py`

Note: `co2_model.pkl` was saved with scikit-learn 1.9.1 (pinned in requirements.txt). If you re-run the notebook on Colab
and save a new pickle, update the pin to the version Colab prints in Step 1.
