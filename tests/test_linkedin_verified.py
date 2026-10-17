"""Tests for evidence-backed LinkedIn URL discovery (no mock data)."""

import pytest
from src.signalpost.web.linkedin import (
    normalize_company_title,
    validate_linkedin_url,
    extract_linkedin_from_brave_result,
    discover_linkedin_urls,
)


class TestNormalizeCompanyTitle:
    def test_lowercase_and_strip(self):
        assert normalize_company_title("  Norges Bank ASA  ") == "norges bank asa"

    def test_remove_special_chars(self):
        assert normalize_company_title("Accenture Ltd.") == "accenture ltd"
        assert normalize_company_title("A/S Telenor") == "as telenor"

    def test_collapse_spaces(self):
        assert normalize_company_title("Statoil  ASA") == "statoil asa"


class TestValidateLinkedinUrl:
    def test_valid_company_url(self):
        assert validate_linkedin_url("https://www.linkedin.com/company/telenor")
        assert validate_linkedin_url("https://linkedin.com/company/12345")

    def test_reject_non_https(self):
        assert not validate_linkedin_url("http://linkedin.com/company/telenor")

    def test_reject_non_company_path(self):
        assert not validate_linkedin_url("https://linkedin.com/in/john-doe")
        assert not validate_linkedin_url("https://linkedin.com/jobs/search")
        assert not validate_linkedin_url("https://linkedin.com/feed/")

    def test_reject_wrong_domain(self):
        assert not validate_linkedin_url("https://linke din.com/company/telenor")

    def test_reject_invalid_input(self):
        assert not validate_linkedin_url(None)
        assert not validate_linkedin_url("")
        assert not validate_linkedin_url(123)


class TestExtractLinkedinFromBraveResult:
    def test_match_with_existing_evidence(self):
        brave_result = {
            'url': 'https://www.linkedin.com/company/telenor',
            'title': 'Telenor ASA | LinkedIn'
        }
        company_name = 'Telenor ASA'
        existing_websites = ['https://www.telenor.com', 'https://www.linkedin.com/company/telenor']

        result = extract_linkedin_from_brave_result(brave_result, company_name, existing_websites)
        assert result == 'https://www.linkedin.com/company/telenor'

    def test_reject_no_evidence(self):
        brave_result = {
            'url': 'https://www.linkedin.com/company/telenor',
            'title': 'Telenor | LinkedIn'
        }
        company_name = 'Telenor ASA'
        existing_websites = ['https://www.telenor.com']  # LinkedIn NOT in evidence

        result = extract_linkedin_from_brave_result(brave_result, company_name, existing_websites)
        assert result is None

    def test_reject_title_mismatch(self):
        brave_result = {
            'url': 'https://www.linkedin.com/company/telenor',
            'title': 'Some Random Company | LinkedIn'
        }
        company_name = 'Telenor ASA'
        existing_websites = ['https://linkedin.com/company/telenor']

        result = extract_linkedin_from_brave_result(brave_result, company_name, existing_websites)
        assert result is None

    def test_reject_invalid_url(self):
        brave_result = {
            'url': 'https://linkedin.com/in/john-doe',  # Person page, not company
            'title': 'Telenor | LinkedIn'
        }
        company_name = 'Telenor ASA'
        existing_websites = ['https://linkedin.com/in/john-doe']

        result = extract_linkedin_from_brave_result(brave_result, company_name, existing_websites)
        assert result is None


class TestDiscoverLinkedinUrls:
    def test_discover_single_match(self):
        brave_results = [
            {
                'url': 'https://www.linkedin.com/company/norges-bank',
                'title': 'Norges Bank | LinkedIn'
            }
        ]
        company_name = 'Norges Bank'
        websites = ['https://www.linkedin.com/company/norges-bank']

        result = discover_linkedin_urls(company_name, brave_results, websites)
        assert result == 'https://www.linkedin.com/company/norges-bank'

    def test_no_results(self):
        result = discover_linkedin_urls('Test Company', [], [])
        assert result is None

    def test_skip_invalid_results(self):
        brave_results = [
            {'url': 'https://linkedin.com/in/john', 'title': 'John Doe'},  # Invalid
            {'url': 'https://linkedin.com/company/test', 'title': 'Test | LinkedIn'}  # Valid
        ]
        company_name = 'Test'
        websites = ['https://linkedin.com/company/test']

        result = discover_linkedin_urls(company_name, brave_results, websites)
        assert result == 'https://linkedin.com/company/test'

    def test_return_first_match(self):
        brave_results = [
            {'url': 'https://linkedin.com/company/test1', 'title': 'Test | LinkedIn'},
            {'url': 'https://linkedin.com/company/test2', 'title': 'Test | LinkedIn'}
        ]
        company_name = 'Test'
        websites = ['https://linkedin.com/company/test1', 'https://linkedin.com/company/test2']

        result = discover_linkedin_urls(company_name, brave_results, websites)
        # Should return first valid match
        assert result is not None
