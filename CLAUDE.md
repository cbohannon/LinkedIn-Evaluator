# LinkedIn Evaluator — Claude Context

## Project Overview
A Python CLI tool that evaluates a LinkedIn profile using the Claude API. The user provides their LinkedIn data export ZIP file and receives a detailed, section-by-section evaluation with actionable recommendations.

## Architecture
The pipeline runs in five stages:

```
ZIP file → extractor.py → parser.py → evaluator.py → reporter.py
                                                           ↓
                                                   console or .md file
```

## Key Files
| File | Purpose |
|------|---------|
| `src/main.py` | CLI entry point (`argparse`), wires pipeline together |
| `src/extractor.py` | Unzips export, locates required/optional CSVs |
| `src/parser.py` | Parses CSVs into a normalized profile dict |
| `src/evaluator.py` | Sends profile to Claude API, returns evaluation text |
| `src/reporter.py` | Adds header and routes output to console or file |
| `prompts/evaluate.md` | Prompt template reference (system prompt lives in evaluator.py) |

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
- Key dependencies: `anthropic`, `python-dotenv`
- API key in `.env` as `ANTHROPIC_API_KEY`
- Model: `claude-opus-4-6`

## Planned Enhancements
- `--role` flag for target role input (e.g. `--role "Senior DevOps Engineer"`)
- Option 2 input: save LinkedIn profile as HTML file
- Scoring dashboard / summary table at top of report
