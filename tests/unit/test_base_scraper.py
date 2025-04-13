import pytest
from bs4 import BeautifulSoup
from webscraper.scrapers.base import BaseScraper

class TestScraper(BaseScraper):
    """Test implementation of BaseScraper for testing"""
    def process_data(self, data):
        return data

def test_base_scraper_initialization():
    """Test BaseScraper initialization with config"""
    config = {
        "type": "test",
        "extractors": {
            "title": {"type": "css", "selector": ".title"},
            "content": {"type": "css", "selector": ".content"},
            "price": {"type": "pattern", "pattern": "£\\d+", "tag": "span"},
            "bedrooms": {"type": "pattern", "pattern": "\\d+\\s*bed", "tag": "span", "extract": "\\d+"}
        }
    }
    scraper = TestScraper(config)
    assert scraper.config == config
    assert scraper.extractors == config["extractors"]

@pytest.mark.parametrize("url,expected_headers", [
    ("https://example.com", {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
])
def test_get_page_headers(url, expected_headers, requests_mock):
    """Test that _get_page method uses correct headers"""
    config = {"type": "test"}
    scraper = TestScraper(config)
    
    # Mock the request
    requests_mock.get(url, text="<html><body>Test</body></html>")
    
    # Make the request
    soup = scraper._get_page(url)
    
    # Verify the request was made with correct headers
    assert requests_mock.last_request.headers["User-Agent"] == expected_headers["User-Agent"]
    assert isinstance(soup, BeautifulSoup)

def test_extract_data():
    """Test both CSS and pattern-based extraction methods"""
    config = {
        "type": "test",
        "extractors": {
            "title": {"type": "css", "selector": ".title"},
            "content": {"type": "css", "selector": ".content"},
            "price": {"type": "pattern", "pattern": "£\\d+", "tag": "span"},
            "bedrooms": {"type": "pattern", "pattern": "\\d+\\s*bed", "tag": "span", "extract": "\\d+"}
        }
    }
    scraper = TestScraper(config)
    
    # Create a test HTML document
    html = """
    <html>
        <body>
            <h1 class="title">Test Title</h1>
            <div class="content">Test Content</div>
            <span>Price: £500</span>
            <span>3 bed property</span>
            <div class="missing">Won't be extracted</div>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract data
    data = scraper._extract_data(soup)
    
    # Verify extracted data
    assert data["title"] == "Test Title"
    assert data["content"] == "Test Content"
    assert data["price"] == "£500"
    assert data["bedrooms"] == "3" 