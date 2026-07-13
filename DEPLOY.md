# Deployment Guide

Same pattern as melanoma-detector: frontend on GitHub Pages, backend on Render.

## Backend (Render)

1. Push this repo to GitHub.
2. Create a new **Web Service** on [Render](https://render.com).
3. Connect the repo — Render will detect `render.yaml`.
4. Ensure `models/skin_model.pth` is committed (or use Git LFS).
5. Note the deployed URL, e.g. `https://skin-condition-detector-api.onrender.com`.

## Frontend (GitHub Pages)

1. In repo **Settings → Pages**, set source to **GitHub Actions** or deploy from `/frontend`.
2. Update `frontend/config.js` with your Render API URL for production.
3. If using the melanoma-detector workflow pattern, add `.github/workflows/deploy-frontend.yml`.

## Verify

```bash
curl https://your-api.onrender.com/health
python scripts/test_api.py https://your-api.onrender.com
```
