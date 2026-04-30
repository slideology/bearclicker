import json
import logging
import os
from typing import Optional

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account


logger = logging.getLogger(__name__)

WEBMASTERS_SCOPE = "https://www.googleapis.com/auth/webmasters"
SITEMAP_SUBMIT_URL = "https://www.googleapis.com/webmasters/v3/sites/{site_url}/sitemaps/{feedpath}"


def _load_service_account_info() -> Optional[dict]:
    """Load Search Console service account credentials from env."""
    raw_json = os.getenv("GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON")
    file_path = os.getenv("GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_FILE")

    if raw_json:
        try:
            return json.loads(raw_json)
        except json.JSONDecodeError as exc:
            logger.error("Invalid GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON: %s", exc)
            return None

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("Failed to load GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_FILE: %s", exc)
            return None

    return None


def is_configured() -> bool:
    return bool(
        os.getenv("GOOGLE_SEARCH_CONSOLE_SITE_URL")
        and (
            os.getenv("GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON")
            or os.getenv("GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_FILE")
        )
    )


def submit_sitemap(
    sitemap_url: Optional[str] = None,
    site_url: Optional[str] = None,
) -> bool:
    """
    Submit sitemap URL to Google Search Console.

    site_url examples:
    - https://bearclicker.net/
    - sc-domain:bearclicker.net
    """
    site_url = site_url or os.getenv("GOOGLE_SEARCH_CONSOLE_SITE_URL")
    sitemap_url = sitemap_url or os.getenv(
        "GOOGLE_SEARCH_CONSOLE_SITEMAP_URL",
        "https://bearclicker.net/sitemap.xml",
    )

    if not site_url:
        logger.info("Google Search Console submit skipped: GOOGLE_SEARCH_CONSOLE_SITE_URL not configured.")
        return False

    service_account_info = _load_service_account_info()
    if not service_account_info:
        logger.info(
            "Google Search Console submit skipped: service account credentials not configured."
        )
        return False

    try:
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=[WEBMASTERS_SCOPE],
        )
        credentials.refresh(Request())

        endpoint = SITEMAP_SUBMIT_URL.format(
            site_url=requests.utils.quote(site_url, safe=""),
            feedpath=requests.utils.quote(sitemap_url, safe=""),
        )

        response = requests.put(
            endpoint,
            headers={
                "Authorization": f"Bearer {credentials.token}",
            },
            timeout=20,
        )

        if response.status_code in (200, 204):
            logger.info(
                "Successfully submitted sitemap to Google Search Console. site=%s sitemap=%s",
                site_url,
                sitemap_url,
            )
            return True

        logger.error(
            "Failed to submit sitemap to Google Search Console. status=%s response=%s",
            response.status_code,
            response.text,
        )
        return False
    except Exception as exc:
        logger.error("Google Search Console sitemap submission error: %s", exc)
        return False
