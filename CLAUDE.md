# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Shell state does not persist between Claude Code Bash calls, so `source venv/bin/activate` has no lasting effect. Call the venv binaries directly. The system `python3` also has Flask installed, so a missing venv can go unnoticed.

```bash
python3 -m venv venv && venv/bin/pip install -r requirements.txt   # setup
venv/bin/python app.py                                             # dev server, http://127.0.0.1:5001, debug + auto-reload
venv/bin/pytest                                                    # all tests
venv/bin/pytest tests/test_file.py::test_name                      # single test
```

No tests exist yet. pytest-flask expects a `conftest.py` that provides an `app` fixture. `app` is a module-level instance (no app factory), so use `from app import app`. No linter or formatter is configured.

## Architecture

Spendly is a personal expense tracker in INR (₹): server-rendered Flask, Jinja2 templates, plain CSS and vanilla JS. It has no frontend framework, no build step and no JS dependencies; keep it that way.

**Tutorial-staged project.** The app is being built in numbered steps. Unimplemented routes in `app.py` return placeholder strings like `"Add expense — coming in Step 7"`. The steps are: 1 database, 3 logout, 4 profile, 7–9 add/edit/delete expense. When implementing a step, replace the placeholder in place instead of adding a parallel route.

- **Routes:** all live in `app.py`, with no blueprints. Templates link with `url_for(...)`, never hard-coded paths.
- **Database:** `database/db.py` is still a stub. The intended design, from its comments, is raw `sqlite3` with no ORM: `get_db()` (row_factory, foreign keys on), `init_db()` (`CREATE TABLE IF NOT EXISTS`) and `seed_db()`. The DB file `expense_tracker.db` is git-ignored. Nothing imports `database` yet.
- **Auth forms:** `login.html` and `register.html` submit with `POST`, but the `/login` and `/register` routes are GET-only, so submitting returns 405 until auth is implemented. `login.html` already renders an `{{ error }}` slot.

### Templates

Every page extends `templates/base.html`, which owns the navbar, the footer (including the Terms/Privacy links) and the `main.js` include. Its blocks are `title`, `head`, `content` and `scripts`. Footer and nav changes go in `base.html`, not in individual pages. `terms.html` and `privacy.html` share the `legal-*` CSS classes.

### CSS (`static/css/style.css`)

There is a single stylesheet, divided by banner comments (`/* --- */ /* Section */`). All colours, fonts and radii are CSS variables in `:root`; reuse them instead of hard-coding values.

- **Two greens:** `--accent` (dark forest) is the brand colour and button hover. `--accent-bright` is used for the hero headline and badge. Use `--accent-bright-ink` for small text on light backgrounds, because `--accent-bright` does not meet 4.5:1 contrast at body sizes.
- **Two type voices:** the landing hero uses DM Sans (600). Other section headings (features, CTA, auth, legal) use `--font-display` (DM Serif Display). Only DM Sans weights 300–600 are loaded from Google Fonts.
- **Responsive:** responsive overrides live together in the "Responsive" section at the end of the file, with breakpoints at 900px and 600px.

### JS (`static/js/main.js`)

`base.html` loads this file on every page, so each feature is an IIFE that returns early when its elements aren't present.

**"See how it works" modal (landing page):** this is a native `<dialog>`. The iframe's real URL is in `data-src` and is only assigned to `src` when the modal opens. On the dialog's `close` event, `src` is reset to `about:blank`. That reset is what stops playback, so keep it if you refactor. The video ID is a placeholder that will be replaced.

## Placeholder content to be aware of

- The contact address in `privacy.html` (`privacy@spendly.example`) is fake.
- `privacy.html` claims passwords are stored hashed and that users can delete their accounts. Neither exists yet, so implement auth to match, or update the policy.
