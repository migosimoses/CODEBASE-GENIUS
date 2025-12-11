<<<<<<< HEAD
# CODEBASE-GENIUS
=======
# Codebase Genius

Local development and demo for the Codebase Genius project.

Quickstart (WSL):

1. Create and activate virtualenv (Python 3.12):

```bash
python -m venv jac-env
source "jac-env/bin/activate"
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI server (UI):

```bash
uvicorn server:app --host 127.0.0.1 --port 5000 --reload
```

4. Open UI: http://127.0.0.1:5000

5. Use the UI to `Generate` (Python supervisor) or `Run Jac` (invokes Jac bridge which POSTs to `/process`).

Files of interest:
- `server.py` — FastAPI server and endpoints
- `agentic_codebase_genius/` — Python supervisor and modules
- `agentic_codebase_genius/*.jac` — Jac stubs and bridge
- `web/` — UI templates and static assets

Notes:
- The Jac bridge calls the FastAPI `/process` endpoint; this is simple and robust for demo purposes.
- To convert to a fully Jac-native pipeline, the Jac agent files need further implementation (they currently contain minimal, buildable stubs).

Next steps I can take for you:
- Implement fuller Jac agents incrementally and test with `jac build`/`jac serve`.
- Add integration tests and a CI workflow.
- Polish UI/UX and capture Jac run logs in the UI (already added).

Tell me which next step to prioritize and I will proceed.
>>>>>>> 0d6c3a7 (Initial Codebase Genius snapshot — cleaned Jac files and placeholders)
