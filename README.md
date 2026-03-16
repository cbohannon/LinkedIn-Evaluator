# LinkedIn Evaluator

A Python CLI tool that evaluates your LinkedIn profile using the Claude API and generates a detailed, actionable report with section-by-section recommendations.

## How It Works

You provide your LinkedIn profile via one of three input methods (see below). The tool sends your profile data to Claude and outputs a markdown report with:

- A **scorecard table** showing per-section scores at a glance
- Section-by-section analysis: Headline, Summary, Experience, Skills, Recommendations
- Top quick wins — the 3 changes to make immediately for the biggest impact

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

---

## Input Methods

### Option 1: `--zip` — LinkedIn Data Export (most complete)

The most structured and reliable input. LinkedIn exports your full profile as a ZIP of CSV files.

**How to get your export:**

1. Go to LinkedIn → **Me** → **Settings & Privacy**
2. Click **Data Privacy** → **Get a copy of your data**
3. Select **Want something in particular?** and check the relevant data categories
4. Request the archive — LinkedIn will email you when it's ready (up to 24 hours)
5. Download the ZIP file

**Usage:**
```bash
# Print report to console
python src/main.py --zip /path/to/linkedin-export.zip

# Save report to a markdown file
python src/main.py --zip /path/to/linkedin-export.zip --output report.md

# Tailor evaluation to a specific target role
python src/main.py --zip /path/to/linkedin-export.zip --role "Senior DevOps Engineer" --output report.md
```

---

### Option 2: `--html` — Saved HTML File

Save your LinkedIn profile page as an HTML file from your browser and pass it directly. Faster than waiting for a data export, but LinkedIn collapses many sections by default, so the saved page may be missing experience details, recommendations, and other content.

**How to save your profile as HTML:**

1. Open your LinkedIn profile in Chrome or Edge
2. Press `Ctrl+S` (Windows) or `Cmd+S` (Mac)
3. Choose **Webpage, Complete** or **Webpage, HTML Only**
4. Save the file

**Usage:**
```bash
python src/main.py --html /path/to/profile.html

# With a target role
python src/main.py --html /path/to/profile.html --role "Product Manager"
```

> **Note:** Because LinkedIn collapses sections before you save, the resulting evaluation may be less detailed than `--zip` or `--url`. Manually expanding all sections before saving will improve results.

---

### Option 3: `--url` — Browser Automation (recommended for quick evaluations)

The easiest option after first-time setup. Provide your LinkedIn profile URL and the tool launches a real browser, automatically expands all collapsed sections, extracts the full visible text, and sends it to Claude.

**One-time setup:**
```bash
pip install playwright
playwright install chromium
```

**Usage:**
```bash
python src/main.py --url "https://www.linkedin.com/in/your-username/"

# With a target role
python src/main.py --url "https://www.linkedin.com/in/your-username/" --role "Staff Engineer"
```

**First run:** A browser window will open. If you are not already logged in to LinkedIn, you will be prompted to log in manually. After logging in, return to the terminal and press Enter. Your session is saved in `.browser_profile/` so subsequent runs log in automatically.

**Subsequent runs:** The browser opens, navigates directly to the profile, expands sections, and closes — no manual steps required.

> **Note:** `--url` works best on your own profile or public profiles. LinkedIn must be able to display the profile while you are logged in.

---

## Output Example

```
# LinkedIn Profile Evaluation

**Name:** Jane Smith
**Headline:** Senior Product Manager | SaaS | B2B
**Target Role:** Director of Product
**Date:** March 04, 2026

---

## Scorecard

| Section                 | Score |
|-------------------------|-------|
| Headline                |  8/10 |
| Summary / About         |  7/10 |
| Experience              |  9/10 |
| Skills                  |  8/10 |
| Recommendations         |  6/10 |
|-------------------------|-------|
| Overall                 |  8/10 |

---

## 1. Overall Score: 8 / 10
...
```

## Privacy

Your LinkedIn data never leaves your machine except for the API call to Anthropic. ZIP files, CSV files, and browser session data are excluded from version control via `.gitignore`. See [Anthropic's privacy policy](https://www.anthropic.com/privacy) for how API data is handled.

