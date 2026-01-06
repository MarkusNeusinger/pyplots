"""Server-side Plausible Analytics for og:image tracking.

Tracks og:image requests from social media bots (Twitter, WhatsApp, etc.)
since bots don't execute JavaScript and can't be tracked client-side.

Uses fire-and-forget pattern to avoid delaying responses.
"""

import asyncio
import logging

import httpx
from fastapi import Request


logger = logging.getLogger(__name__)

PLAUSIBLE_ENDPOINT = "https://plausible.io/api/event"
DOMAIN = "pyplots.ai"

# All platforms from nginx.conf bot detection (27 total)
PLATFORM_PATTERNS = {
    # Social Media
    "twitter": "twitterbot",
    "facebook": "facebookexternalhit",
    "linkedin": "linkedinbot",
    "pinterest": "pinterestbot",
    "reddit": "redditbot",
    "tumblr": "tumblr",
    "mastodon": "mastodon",
    # Messaging Apps
    "slack": "slackbot",
    "discord": "discordbot",
    "telegram": "telegrambot",
    "whatsapp": "whatsapp",
    "signal": "signal",
    "viber": "viber",
    "skype": "skypeuripreview",
    "teams": "microsoft teams",
    "snapchat": "snapchat",
    # Search Engines
    "google": "googlebot",
    "bing": "bingbot",
    "yandex": "yandexbot",
    "duckduckgo": "duckduckbot",
    "baidu": "baiduspider",
    "apple": "applebot",
    # Link Preview Services
    "embedly": "embedly",
    "quora": "quora link preview",
    "outbrain": "outbrain",
    "rogerbot": "rogerbot",
    "showyoubot": "showyoubot",
}


def detect_platform(user_agent: str) -> str:
    """Detect platform from User-Agent string.

    Args:
        user_agent: The User-Agent header value

    Returns:
        Platform name (e.g., 'twitter', 'whatsapp') or 'unknown'
    """
    ua_lower = user_agent.lower()
    for platform, pattern in PLATFORM_PATTERNS.items():
        if pattern in ua_lower:
            return platform
    return "unknown"


async def _send_plausible_event(user_agent: str, client_ip: str, name: str, url: str, props: dict) -> None:
    """Internal: Send event to Plausible (called as background task).

    Args:
        user_agent: Original User-Agent header
        client_ip: Client IP for geolocation
        name: Event name
        url: Page URL
        props: Event properties
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                PLAUSIBLE_ENDPOINT,
                headers={"User-Agent": user_agent, "X-Forwarded-For": client_ip, "Content-Type": "application/json"},
                json={"name": name, "url": url, "domain": DOMAIN, "props": props},
            )
    except Exception as e:
        logger.debug(f"Plausible tracking failed (non-critical): {e}")


def track_og_image(
    request: Request,
    page: str,
    spec: str | None = None,
    library: str | None = None,
    filters: dict[str, str] | None = None,
) -> None:
    """Track og:image request (fire-and-forget).

    Sends event to Plausible in background without blocking response.

    Args:
        request: FastAPI request for headers
        page: Page type ('home', 'catalog', 'spec_overview', 'spec_detail')
        spec: Spec ID (optional)
        library: Library ID (optional)
        filters: Query params for filtered home page (e.g., {'lib': 'plotly', 'dom': 'statistics'})
    """
    user_agent = request.headers.get("user-agent", "")
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    platform = detect_platform(user_agent)

    # Build URL based on page type
    if page == "home":
        url = "https://pyplots.ai/"
    elif page == "catalog":
        url = "https://pyplots.ai/catalog"
    elif spec is not None and library:
        url = f"https://pyplots.ai/{spec}/{library}"
    elif spec is not None:
        url = f"https://pyplots.ai/{spec}"
    else:
        # Fallback: missing spec for a spec-based page
        url = "https://pyplots.ai/"

    props: dict[str, str] = {"page": page, "platform": platform}
    if spec:
        props["spec"] = spec
    if library:
        props["library"] = library
    if filters:
        # Add each filter as separate prop (e.g., filter_lib, filter_dom)
        # This handles comma-separated values like lib=plotly,matplotlib
        for key, value in filters.items():
            props[f"filter_{key}"] = value

    # Fire-and-forget: create task without awaiting
    asyncio.create_task(_send_plausible_event(user_agent, client_ip, "og_image_view", url, props))
