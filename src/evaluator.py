import json

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """You are an expert LinkedIn profile coach with deep knowledge of personal branding, \
recruiting practices, and career development. Your job is to evaluate LinkedIn profiles and provide \
specific, actionable recommendations to help professionals stand out.

When evaluating a profile, be honest and constructive. Point to exact text that could be improved \
and explain why. Avoid generic advice — every recommendation should be specific to this profile.

Structure your evaluation with exactly these sections:
1. Overall Score (out of 10) with a 2-3 sentence summary
2. Headline — clarity, keywords, value proposition
3. Summary/About — storytelling, hook, length, call to action
4. Experience — bullet quality, quantified achievements, action verbs
5. Skills — relevance, coverage, notable gaps
6. Recommendations — social proof assessment (if none, note the impact)
7. Quick Wins — the top 3 changes to make immediately for the biggest impact

Return your response as a single JSON object with exactly this structure:
{
  "scores": {
    "headline": <int 1-10>,
    "summary": <int 1-10>,
    "experience": <int 1-10>,
    "skills": <int 1-10>,
    "recommendations": <int 1-10>,
    "overall": <int 1-10>
  },
  "evaluation": "<full markdown evaluation text as a single escaped string>"
}

The "evaluation" field must contain the complete 7-section evaluation exactly as you would normally write it. Do not abbreviate. Return only the JSON object — no additional text before or after it.
"""


def _parse_response(raw: str) -> dict:
    """Parse Claude's JSON response. Falls back gracefully on failure."""
    try:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {"scores": {}, "evaluation": raw}


def evaluate(profile: dict) -> dict:
    """
    Send the profile dict to Claude and return the evaluation text.
    """
    client = Anthropic()

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please evaluate the following LinkedIn profile:\n\n{_format_profile(profile)}",
            }
        ],
    )

    return _parse_response(message.content[0].text)


def evaluate_raw(text: str) -> dict:
    """
    Send raw profile text (e.g. extracted from HTML) to Claude and return the evaluation.
    """
    client = Anthropic()

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please evaluate the following LinkedIn profile:\n\n{text}",
            }
        ],
    )

    return _parse_response(message.content[0].text)


def _format_profile(profile: dict) -> str:
    """Format the profile dict as readable text for the prompt."""
    lines = []

    name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    if name:
        lines.append(f"Name: {name}")

    if profile.get("headline"):
        lines.append(f"Headline: {profile['headline']}")

    if profile.get("industry"):
        lines.append(f"Industry: {profile['industry']}")

    if profile.get("location"):
        lines.append(f"Location: {profile['location']}")

    if profile.get("summary"):
        lines.append(f"\nSummary:\n{profile['summary']}")

    if profile.get("positions"):
        lines.append("\nExperience:")
        for pos in profile["positions"]:
            end = pos["finished_on"] or "Present"
            lines.append(f"  - {pos['title']} at {pos['company']} ({pos['started_on']} - {end})")
            if pos.get("description"):
                lines.append(f"    {pos['description']}")

    if profile.get("education"):
        lines.append("\nEducation:")
        for edu in profile["education"]:
            lines.append(f"  - {edu['degree']} at {edu['school']} ({edu['start_date']} - {edu['end_date']})")

    if profile.get("skills"):
        lines.append(f"\nSkills: {', '.join(profile['skills'])}")

    if profile.get("recommendations"):
        lines.append(f"\nRecommendations ({len(profile['recommendations'])}):")
        for rec in profile["recommendations"]:
            name = f"{rec['first_name']} {rec['last_name']}".strip()
            lines.append(f"  - From {name} ({rec['job_title']} at {rec['company']}):")
            lines.append(f"    \"{rec['text']}\"")

    return "\n".join(lines)
