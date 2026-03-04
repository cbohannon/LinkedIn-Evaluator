import csv
import io
from pathlib import Path


def parse(files: dict[str, Path]) -> dict:
    """
    Parse LinkedIn CSV files into a normalized profile dict.
    """
    profile = {}

    if "profile" in files:
        profile.update(_parse_profile(files["profile"]))

    if "positions" in files:
        profile["positions"] = _parse_positions(files["positions"])

    if "education" in files:
        profile["education"] = _parse_education(files["education"])

    if "skills" in files:
        profile["skills"] = _parse_skills(files["skills"])

    if "recommendations" in files:
        profile["recommendations"] = _parse_recommendations(files["recommendations"])

    return profile


def _read_csv(path: Path) -> list[dict]:
    """
    Read a LinkedIn CSV into a list of dicts.

    LinkedIn exports sometimes prepend "Notes:" metadata rows before the
    actual header. This skips those and finds the real header row.
    Also handles the UTF-8 BOM that LinkedIn sometimes includes.
    """
    with open(path, encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Skip leading notes/blank lines to find the real CSV header
    start = 0
    for i, line in enumerate(lines):
        if line.strip() == "" or line.strip().startswith("Notes:"):
            continue
        start = i
        break

    content = "".join(lines[start:])
    reader = csv.DictReader(io.StringIO(content))
    return [row for row in reader]


def _parse_profile(path: Path) -> dict:
    rows = _read_csv(path)
    if not rows:
        return {}
    row = rows[0]  # Profile is always a single row
    return {
        "first_name": row.get("First Name", "").strip(),
        "last_name": row.get("Last Name", "").strip(),
        "headline": row.get("Headline", "").strip(),
        "summary": row.get("Summary", "").strip(),
        "industry": row.get("Industry", "").strip(),
        "location": row.get("Geo Location", "").strip(),
    }


def _parse_positions(path: Path) -> list[dict]:
    rows = _read_csv(path)
    return [
        {
            "title": row.get("Title", "").strip(),
            "company": row.get("Company Name", "").strip(),
            "location": row.get("Location", "").strip(),
            "started_on": row.get("Started On", "").strip(),
            "finished_on": row.get("Finished On", "").strip(),
            "description": row.get("Description", "").strip(),
        }
        for row in rows
    ]


def _parse_education(path: Path) -> list[dict]:
    rows = _read_csv(path)
    return [
        {
            "school": row.get("School Name", "").strip(),
            "degree": row.get("Degree Name", "").strip(),
            "start_date": row.get("Start Date", "").strip(),
            "end_date": row.get("End Date", "").strip(),
            "notes": row.get("Notes", "").strip(),
            "activities": row.get("Activities", "").strip(),
        }
        for row in rows
    ]


def _parse_skills(path: Path) -> list[str]:
    rows = _read_csv(path)
    return [row.get("Name", "").strip() for row in rows if row.get("Name", "").strip()]


def _parse_recommendations(path: Path) -> list[dict]:
    rows = _read_csv(path)
    return [
        {
            "first_name": row.get("First Name", "").strip(),
            "last_name": row.get("Last Name", "").strip(),
            "company": row.get("Company", "").strip(),
            "job_title": row.get("Job Title", "").strip(),
            "text": row.get("Text", "").strip(),
        }
        for row in rows
    ]
