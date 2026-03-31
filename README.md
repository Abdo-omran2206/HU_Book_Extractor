![HU Book banner](src/banner.svg)

# HU Book Extractor

**HU Book** (HU Book Extractor) is a small Python tool that turns web-hosted books built from static HTML into a **single PDF**, using a headless browser for each page and merging the results. The output filename comes from the book’s title when available.

## Features

- Checks that the book is reachable and reads its title and page list
- Renders each page to PDF with Playwright (Chromium)
- Merges everything into one PDF with PyPDF2

## Requirements

- Python 3.10+ recommended
- Standard library modules (`asyncio`, `urllib`, `xml`, `os`, …) — no extra pip packages for those
- Chromium for Playwright (installed through Playwright’s CLI — see [Playwright for Python](https://playwright.dev/python/docs/intro))

## Setup

### Option A — automated (`setup.py`)

From the project root:

```bash
python setup.py
```

This runs an editable install (`pip install -e .`) from `requirements.txt`, then installs the Chromium build Playwright needs.

### Option B — manual

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

On macOS/Linux, use `source .venv/bin/activate`.

### Package install (deps only)

```bash
pip install -e .
```

If you do not use `python setup.py`, run `playwright install chromium` once yourself.

## Usage

```bash
python main.py
```

When asked, paste the **root address of the book** on the web—the same kind of link you would use to open the book in a browser (the tool adjusts small formatting differences automatically). Confirm with `y` to start. The PDF is written in the current working directory.

## Project layout

| Path | Role |
|------|------|
| `main.py` | Interactive CLI and flow |
| `setup.py` | Optional setup: editable install + Playwright Chromium |
| `requirements.txt` | Third-party dependencies |
| `lib/ebooks_scraper.py` | Core logic: network fetch, page discovery, PDF build |
| `lib/__init__.py` | Package marker |
| `src/logo.svg` | Square logo |
| `src/banner.svg` | README banner |

## Notes

- The site must serve the book in a way this project supports; unsupported layouts will fail validation.
- During a run, temporary PDFs are created and removed after the final file is written.
- On Windows, the CLI uses ANSI colors; use a modern terminal if they do not show.

## License

Add a license file if you distribute this project.

## Author

**AkiraOmran** — for HU students.
