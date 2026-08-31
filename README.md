# dnd-plus-plus

Compact TTRPG campaign manager focused on server-rendered pages, small frontend controls, and test-driven behavior.

## Quick overview

- Purpose: lightweight app for managing campaigns, characters, and sharable pages.
- Architecture: modular Python backend (API endpoints under `ttrpg/api/`), server templates in `ttrpg/templates/`, static assets in `ttrpg/static/`, and small client-side JS in `ttrpg/static/js/`.

## Tech

- Python 3.x (project metadata in `pyproject.toml`)
- Tests: `pytest` under the `tests/` directory
- Scripts: small CLI helpers in `bin/` for install/run tasks

## Run & test

Clone and install editable package, then run tests:

```bash
pip install -e .
pytest -q
```

Alternatively use the helper scripts in `bin/` (e.g., `bin/ttrpgrun`) for local runs.
