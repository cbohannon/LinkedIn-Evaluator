# LinkedIn Evaluator

A Python CLI tool that evaluates your LinkedIn profile using the Claude API and generates a detailed, actionable report with section-by-section recommendations.

## How It Works

You provide your LinkedIn data export ZIP file. The tool parses the relevant CSV files, sends the structured profile data to Claude, and outputs a markdown report covering:

- Overall score
- Headline analysis
- Summary / About section
- Experience bullets
- Skills gaps
- Recommendations (social proof)
- Top quick wins

## Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com)

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env`:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Getting Your LinkedIn Data Export

1. Go to LinkedIn → **Me** → **Settings & Privacy**
2. Click **Data Privacy** → **Get a copy of your data**
3. Select **Want something in particular?** and check the relevant data categories
4. Request the archive — LinkedIn will email you when it's ready (up to 24 hours)
5. Download the ZIP file

## Usage

```bash
# Print report to console
python src/main.py --zip /path/to/linkedin-export.zip

# Save report to a markdown file
python src/main.py --zip /path/to/linkedin-export.zip --output report.md
```

## Output Example

```
# LinkedIn Profile Evaluation

**Name:** Jane Smith
**Headline:** Senior Product Manager | SaaS | B2B
**Date:** March 04, 2026

---

## 1. Overall Score: 8 / 10
...
```

## Privacy

Your LinkedIn data never leaves your machine except for the API call to Anthropic. The ZIP file and any CSV files are excluded from version control via `.gitignore`. See [Anthropic's privacy policy](https://www.anthropic.com/privacy) for how API data is handled.

## Planned Enhancements

- `--role` flag to tailor recommendations to a specific target role
- HTML input option (save your LinkedIn profile as `.html` for instant evaluation without waiting for the data export)
