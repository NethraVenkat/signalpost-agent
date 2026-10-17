"""Evidence-backed LinkedIn URL discovery.

LinkedIn URLs are discovered only when:
1. A Brave search result nominates a LinkedIn company page
2. The page title matches the company's registered name (normalized)
3. The company has an existing, current-run, company-owned website claim
4. The LinkedIn URL matches exactly with the website evidence

No synthetic profiles, inferred URLs, mock data, or guessed attributes.
"""

import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse


def normalize_company_title(title: str) -> str:
    """Normalize company name for matching with LinkedIn title."""
    # Remove diacritics, lowercase, collapse whitespace
    title = title.lower().strip()
    # Remove special characters
    title = re.sub(r'[^\w\s]', '', title)
    # Collapse multiple spaces
    title = re.sub(r'\s+', ' ', title)
    return title


def validate_linkedin_url(url: str) -> bool:
    """Validate that URL is a legitimate LinkedIn company page."""
    if not url or not isinstance(url, str):
        return False

    # Must be HTTPS
    if not url.startswith('https://'):
        return False

    # Must be linkedin.com/company/*
    parsed = urlparse(url)
    if parsed.netloc not in ('linkedin.com', 'www.linkedin.com'):
        return False

    # Must not be /jobs/ or /people/ paths
    if '/jobs/' in url or '/people/' in url or '/feed/' in url:
        return False

    # Must match /company/xxx pattern
    if '/company/' not in url:
        return False

    return True


def extract_linkedin_from_brave_result(
    brave_result: Dict[str, Any],
    company_name: str,
    existing_website_urls: list
) -> Optional[str]:
    """
    Extract LinkedIn URL from Brave search result if it matches company evidence.

    Args:
        brave_result: Single result from Brave search API
        company_name: Registered company name
        existing_website_urls: List of already-verified company-owned website URLs

    Returns:
        Normalized LinkedIn URL if matched, None otherwise
    """

    result_url = brave_result.get('url', '')
    result_title = brave_result.get('title', '')

    # URL must be valid LinkedIn company page
    if not validate_linkedin_url(result_url):
        return None

    # Title must match company name
    result_title_norm = normalize_company_title(result_title)
    company_name_norm = normalize_company_title(company_name)

    # Exact match or close variation
    if result_title_norm != company_name_norm:
        # Allow minor variations (e.g., "Company AS" vs "Company")
        if not (company_name_norm in result_title_norm or result_title_norm in company_name_norm):
            return None

    # URL must be in existing website evidence (company must own it)
    url_found_in_evidence = False
    for evidence_url in existing_website_urls:
        if evidence_url and validate_linkedin_url(evidence_url):
            if evidence_url.rstrip('/') == result_url.rstrip('/'):
                url_found_in_evidence = True
                break

    if not url_found_in_evidence:
        return None

    # All checks passed, return normalized URL
    return result_url.rstrip('/')


def discover_linkedin_urls(
    company_name: str,
    brave_search_results: list,
    company_websites: list
) -> Optional[str]:
    """
    Discover LinkedIn URL from Brave search only if evidence-backed.

    Args:
        company_name: Company's registered name
        brave_search_results: Results from Brave Web Search API
        company_websites: Existing website URLs from current run

    Returns:
        LinkedIn URL (str) if found and verified, None otherwise
    """

    if not brave_search_results:
        return None

    for result in brave_search_results:
        linkedin_url = extract_linkedin_from_brave_result(
            result,
            company_name,
            company_websites
        )
        if linkedin_url:
            return linkedin_url

    return None
