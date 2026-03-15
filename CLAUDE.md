# LinkedIn Evaluator — Claude Context

## Project Overview
A Python CLI tool that evaluates a LinkedIn profile using the Claude API. Supports three input modes: LinkedIn data export ZIP, saved HTML file, and live browser automation via URL.

## Architecture

### `--zip` pipeline
```
ZIP file → extractor.py → parser.py → evaluator.py → reporter.py
                                                           ↓
                                                   console or .md file
```

### `--html` pipeline
```
HTML file → html_parser.py → evaluator.py (evaluate_raw) → reporter.py
```

### `--url` pipeline
```
URL → browser.py (Playwright) → evaluator.py (evaluate_raw) → reporter.py
```

All three modes converge at `evaluator.py` and `reporter.py`. The `--zip` path uses `evaluate(profile_dict)`; `--html` and `--url` use `evaluate_raw(text)`.

## Key Files
| File | Purpose |
|------|---------|
| `src/main.py` | CLI entry point (`argparse`), wires pipeline together |
| `src/extractor.py` | Unzips export, locates required/optional CSVs |
| `src/parser.py` | Parses CSVs into a normalized profile dict |
| `src/html_parser.py` | Extracts visible text from a saved HTML file |
| `src/browser.py` | Playwright browser automation — fetches and expands a live LinkedIn profile |
| `src/evaluator.py` | Sends profile to Claude API, returns evaluation text |
| `src/reporter.py` | Adds header and routes output to console or file |
| `prompts/evaluate.md` | Prompt template reference (system prompt lives in evaluator.py) |

## `--html` Mode Notes
- Uses `html_parser.py` (`parse_html(path) -> str`) to extract visible text via BeautifulSoup
- LinkedIn collapses sections before the page is saved, so the extracted text may be incomplete
- Results are less detailed than `--zip` or `--url` unless sections are manually expanded before saving

## `--url` Mode Notes
- Uses `browser.py` (`fetch_profile(url) -> str`)
- Requires one-time setup: `pip install playwright && playwright install chromium`
- Always runs `headless=False` — LinkedIn is more likely to block headless browsers
- Uses `--disable-blink-features=AutomationControlled` to suppress Chrome's automation flag
- Session is persisted in `.browser_profile/` (gitignored) — first run may require manual login
- `_is_login_page()` detects `/login`, `/checkpoint/`, and `/authwall` redirects
- `_expand_sections()` clicks all "see more" / "show more" buttons before extracting text
- Text is extracted with `page.inner_text("body")` — respects CSS visibility, excludes hidden elements
- `_validate_url()` enforces `linkedin.com` domain and `/in/` path before launching the browser

## LinkedIn Export CSV Files
| Key | Filename | Required |
|-----|----------|----------|
| profile | Profile.csv | Yes |
| positions | Positions.csv | Yes |
| education | Education.csv | Yes |
| skills | Skills.csv | Yes |
| recommendations | Recommendations_Received.csv | No |

## Important Notes
- LinkedIn CSVs sometimes include "Notes:" metadata rows before the real header — `_read_csv()` in `parser.py` skips these
- LinkedIn CSVs use UTF-8 with BOM — handled via `encoding="utf-8-sig"`
- The system prompt in `evaluator.py` enforces a strict 7-section output structure
- `max_tokens=4096` — needed for complete evaluations on large profiles
- Temp extraction directory is always cleaned up in `main.py`'s `finally` block
- All progress messages go to `stderr`; report content goes to `stdout`

## Environment
- Python 3.12
- Key dependencies: `anthropic`, `python-dotenv`, `playwright`
- API key in `.env` as `ANTHROPIC_API_KEY`
- Model: `claude-opus-4-6`

## Planned Enhancements
- `--role` flag for target role input (e.g. `--role "Senior DevOps Engineer"`)
- Scoring dashboard / summary table at top of report
