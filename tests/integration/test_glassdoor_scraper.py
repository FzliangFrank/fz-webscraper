import pytest
from webscraper.scrapers.glassdoor import GlassdoorScraper

@pytest.fixture
def mock_glassdoor_page(requests_mock):
    """Fixture to mock Glassdoor job listing page"""
    html_content = """
    <html>
        <body>
            <h1 class="job-title">Software Engineer</h1>
            <div class="employer-name">Example Company</div>
            <div class="location">San Francisco, CA</div>
            <div class="salary-estimate">$100K-$150K</div>
            <div class="job-description">Example job description</div>
        </body>
    </html>
    """
    url = "https://www.glassdoor.com/job-listing/example"
    requests_mock.get(url, text=html_content)
    return url

def test_glassdoor_scraping(mock_glassdoor_page):
    """Test scraping a Glassdoor job listing"""
    config = {
        "type": "job_listing",
        "selectors": {
            "job_title": ".job-title",
            "company_name": ".employer-name",
            "location": ".location",
            "salary": ".salary-estimate",
            "job_description": ".job-description"
        }
    }
    
    scraper = GlassdoorScraper(config)
    data = scraper.scrape(mock_glassdoor_page)
    
    assert data["job_title"] == "Software Engineer"
    assert data["company_name"] == "Example Company"
    assert data["location"] == "San Francisco, CA"
    assert data["salary"] == "$100K-$150K"
    assert data["job_description"] == "Example job description" 