# Copilot instructions

## Project overview

Spendly is a small Flask app for tracking personal expenses in INR (₹). The repository is intentionally lightweight: server-rendered HTML via Jinja templates, one stylesheet, one JavaScript file, and a SQLite database layer to be implemented in the tutorial steps.

## Build, test, and lint commands

Use the project virtual environment instead of the system Python:

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt

venv/bin/python app.py
# runs the Flask app on http://127.0.0.1:5001

venv/bin/pytest
# full test suite
venv/bin/pytest tests/test_file.py::test_name
# run one test by node ID
```

There is no configured linter or formatter in this repo. `pytest-flask` is installed, and the project is set up for pytest-based tests, but there are no tests checked in yet.

## Architecture

- `app.py` is the entire Flask app: routes are defined here, with no blueprints or app factory.
- `templates/` contains the UI. Every page should extend `templates/base.html`, which owns the shared navbar, footer, and `main.js` include.
- `templates/base.html` is the source of truth for the common layout; individual pages only override blocks such as `title`, `head`, `content`, and `scripts`.
- `static/css/style.css` is the single stylesheet for the app. Styling is organized by section comments; colors, fonts, and radii are defined in `:root` variables.
- `static/js/main.js` is the shared frontend script. Features are organized as small IIFEs that exit early when their target elements do not exist.
- `database/db.py` is intended to provide the raw SQLite access layer (`get_db()`, `init_db()`, `seed_db()`) with `sqlite3` and row_factory enabled. The file is currently a stub, so database work belongs there when implementing the tutorial steps.
- The project is tutorial-staged: placeholder routes in `app.py` are intentionally left as "coming in Step ..." messages. When implementing a step, replace the placeholder in place instead of adding a separate parallel route.

## Conventions specific to this repo

- Keep all routes in `app.py`; avoid creating blueprints or distributing route definitions across modules.
- Use `url_for(...)` for internal links and asset paths instead of hard-coded paths.
- Prefer server-rendered Jinja templates over client-side rendering. There is no JS framework or build pipeline to maintain.
- Follow the shared layout in `templates/base.html` and keep footer/nav updates there rather than in individual templates.
- The CSS uses section-based organization and CSS variables. Reuse existing variables instead of hard-coded palette values.
- The frontend JS follows a simple pattern: one `main.js` file with self-contained IIFEs; the landing-page video modal intentionally loads the iframe `src` only when opened and clears it on close to stop playback.
- Auth pages already render form submissions with `POST`, but the routes are still GET-only until the authentication step is implemented; do not assume the forms are complete without the backend.
- Use the virtual environment (`venv/bin/...`) for Python, pytest, and Flask commands to match the project setup.

## Repo guidance and existing docs

This repository currently has `CLAUDE.md` as the main project-level guidance file. Use it as the source for environment-specific setup details, especially the expected Flask + SQLite tutorial structure.

## When making changes

- Prefer surgical edits that match the existing tutorial structure and route naming.
- Keep CSS and JS changes within the existing single-file conventions unless the task explicitly requires a new file.
- Do not add a frontend framework or build tooling; this project intentionally stays dependency-light.

## Useful validation pattern

If a feature is added to a route or template, validate it with a focused Flask or pytest check rather than broad refactors. For example:

```bash
venv/bin/pytest tests/test_login.py::test_login_page_renders
```

If no tests exist yet for a change, prefer a small, direct sanity check that matches the app behavior instead of introducing unrelated infrastructure.
