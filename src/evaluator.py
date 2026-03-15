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
"""


def evaluate(profile: dict) -> str:
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

    return message.content[0].text


def evaluate_raw(text: str) -> str:
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

    return message.content[0].text


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
