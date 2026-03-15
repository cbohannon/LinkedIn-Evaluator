"""
browser.py — Playwright-based LinkedIn profile fetcher.

Requires one-time setup:
    pip install playwright
    playwright install chromium
"""

import sys
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


_PROJECT_ROOT = Path(__file__).parent.parent
BROWSER_PROFILE_DIR = _PROJECT_ROOT / ".browser_profile"

_PAGE_LOAD_TIMEOUT = 15_000
_EXPAND_WAIT_MS = 500

# Inline-expansion button text patterns (expand in place, no navigation)
_EXPAND_BUTTON_TEXTS = ["see more", "show more"]


def fetch_profile(url: str) -> str:
    """
    Open a LinkedIn profile URL in a persistent browser session,
    expand all collapsed sections, and return the full visible text.

    On first run, a visible browser opens for manual login.
    On subsequent runs, the saved session is reused automatically.
    """
    _validate_url(url)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_PROFILE_DIR),
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.new_page()
        try:
            _navigate_and_authenticate(page, url)
            _expand_sections(page)
            text = page.inner_text("body")
        finally:
            context.close()

    return text


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"URL must start with http:// or https://: {url}")
    if "linkedin.com" not in parsed.netloc:
        raise ValueError(f"URL does not appear to be a LinkedIn URL: {url}")
    if "/in/" not in parsed.path:
        raise ValueError(
            f"URL does not appear to be a LinkedIn profile (expected /in/...): {url}"
        )


def _navigate_and_authenticate(page, url: str) -> None:
    print(f"Opening LinkedIn profile: {url}", file=sys.stderr)
    try:
        page.goto(url, timeout=_PAGE_LOAD_TIMEOUT, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        raise RuntimeError(
            "Timed out waiting for LinkedIn to load. "
            "Check your internet connection and try again."
        )

    page.wait_for_timeout(1500)

    if _is_login_page(page):
        print("\nLinkedIn requires you to log in.", file=sys.stderr)
        print("Please log in in the browser window that just opened,", file=sys.stderr)
        print("then come back here and press Enter to continue...", file=sys.stderr)
        input()

        try:
            page.goto(url, timeout=_PAGE_LOAD_TIMEOUT, wait_until="domcontentloaded")
        except PlaywrightTimeoutError:
            raise RuntimeError("Timed out after login. Please try again.")

        page.wait_for_timeout(1500)

        if _is_login_page(page):
            raise RuntimeError(
                "Still on the login page after you pressed Enter. "
                "Please ensure you are fully logged in before pressing Enter."
            )

    if "/in/" not in page.url.lower():
        raise RuntimeError(
            f"Unexpected page after navigation. Current URL: {page.url}\n"
            "LinkedIn may have blocked the request or the profile may not exist."
        )

    print("Profile page loaded.", file=sys.stderr)


def _is_login_page(page) -> bool:
    if page.locator("#login-form").count() > 0:
        return True
    current_url = page.url.lower()
    return "/login" in current_url or "/checkpoint/" in current_url or "/authwall" in current_url


def _expand_sections(page) -> None:
    print("Expanding collapsed sections...", file=sys.stderr)
    expanded_count = 0

    for text_pattern in _EXPAND_BUTTON_TEXTS:
        buttons = page.get_by_role("button").filter(has_text=text_pattern)
        count = buttons.count()
        for i in range(count):
            btn = buttons.nth(i)
            try:
                btn.scroll_into_view_if_needed(timeout=2000)
                btn.click(timeout=2000)
                expanded_count += 1
                page.wait_for_timeout(_EXPAND_WAIT_MS)
            except Exception:
                continue

    print(f"Expanded {expanded_count} section(s).", file=sys.stderr)
