import sys
from datetime import date
from pathlib import Path


def report(evaluation: str, profile: dict, output: str = "console") -> None:
    """
    Output the evaluation as a formatted markdown report.

    Args:
        evaluation: Raw text returned by Claude
        profile: Parsed profile dict (used for the report header)
        output: "console" to print, or a file path to save as markdown
    """
    content = _build_report(evaluation, profile)

    if output == "console":
        print(content)
    else:
        dest = Path(output)
        dest.write_text(content, encoding="utf-8")
        print(f"Report saved to {dest}", file=sys.stderr)


def _build_report(evaluation: str, profile: dict) -> str:
    name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    headline = profile.get("headline", "")
    today = date.today().strftime("%B %d, %Y")

    header_lines = [
        "# LinkedIn Profile Evaluation",
        "",
        f"**Name:** {name}" if name else "",
        f"**Headline:** {headline}" if headline else "",
        f"**Date:** {today}",
        "",
        "---",
        "",
    ]

    header = "\n".join(line for line in header_lines if line is not None)
    return header + evaluation
