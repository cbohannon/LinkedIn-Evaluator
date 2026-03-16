import sys
from datetime import date
from pathlib import Path

_SCORE_LABELS = [
    ("headline",        "Headline"),
    ("summary",         "Summary / About"),
    ("experience",      "Experience"),
    ("skills",          "Skills"),
    ("recommendations", "Recommendations"),
]


def _build_scorecard(scores: dict) -> str:
    rows = []
    for key, label in _SCORE_LABELS:
        if key in scores:
            rows.append(f"| {label:<22} | {scores[key]:>2}/10 |")

    return "\n".join([
        "## Scorecard\n",
        f"| {'Section':<22} | Score |",
        f"|{'-'*24}|-------|",
        *rows,
        f"|{'-'*24}|-------|",
        f"| {'Overall':<22} | {scores.get('overall', '?'):>2}/10 |\n",
    ])


def report(evaluation: dict, profile: dict, output: str = "console") -> None:
    """
    Output the evaluation as a formatted markdown report.

    Args:
        evaluation: Dict with 'scores' and 'evaluation' keys returned by Claude
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


def _build_report(evaluation: dict, profile: dict) -> str:
    scores = evaluation.get("scores", {})
    text = evaluation.get("evaluation", "")

    name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    headline = profile.get("headline", "")
    today = date.today().strftime("%B %d, %Y")

    lines = [
        "# LinkedIn Profile Evaluation",
        "",
        f"**Name:** {name}" if name else "",
        f"**Headline:** {headline}" if headline else "",
        f"**Date:** {today}",
        "",
        "---",
        "",
    ]

    lines = [line for line in lines if line is not None]

    if scores:
        lines.append(_build_scorecard(scores))
        lines.append("---\n")

    lines.append(text)
    return "\n".join(lines)
