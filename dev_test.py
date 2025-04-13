"""
Development script for testing the web scraper package.
This script provides quick ways to test scraping from both supported websites.
"""
from webscraper import scrape_url
from webscraper.notion_client import NotionManager
import json
from colorama import Fore, Style

def print_status(message, status = 'msg'):
    """Print a message with color based on status"""
    if status == 'msg':
        print(Fore.GREEN + message + Style.RESET_ALL)
    elif status == 'warn':
        print(Fore.YELLOW + message + Style.RESET_ALL)
    elif status == 'error':
        print(Fore.RED + message + Style.RESET_ALL)

def test_notion_integration(data, site_type):
    """Test adding scraped data to Notion database"""
    # Debug logging
    print_status("Debug: Checking data types:", 'msg')
    for key, value in data.items():
        print_status(f"{key}: {value} (type: {type(value)})", 'msg')

    try:
        notion_manager = NotionManager(site_type)
        result = notion_manager.add_entry(data)
        print_status(f"Successfully added {site_type} data to Notion!", 'msg')
        print_status(f"Created page ID: {result['id']}", 'msg')
    except Exception as e:
        print_status(f"Error adding to Notion: {e}", 'error')

def test_glassdoor():
    """Test scraping a Glassdoor job listing"""
    # Replace with an actual Glassdoor job listing URL
    url = "https://www.glassdoor.co.uk/Job/index.htm"
    try:
        data = scrape_url(url, "glassdoor")
        print_status("Glassdoor Scraping Results:", 'msg')
        print(json.dumps(data, indent=2))
        test_notion_integration(data, "glassdoor")
    except Exception as e:
        print_status(f"Error scraping Glassdoor: {e}", 'error')

def test_rightmove():
    """Test scraping a Rightmove property listing"""
    # Replace with an actual Rightmove property listing URL
    url = "https://www.rightmove.co.uk/properties/159472709#/?channel=RES_LET"
    try:
        data = scrape_url(url, "rightmove")
        print_status("Rightmove Scraping Results:", 'msg')
        print(json.dumps(data, indent=2))
        # test_notion_integration(data, "rightmove")
    except Exception as e:
        print_status(f"Error scraping Rightmove: {e}", 'error')
def test_spareroom():
    url = "https://www.spareroom.co.uk/flatshare/london/london_n7/17320490"
    try:
        data = scrape_url(url, "spareroom")
        print_status("Spareroom Scraping Results:", 'msg')
        print(json.dumps(data, indent=2))
        test_notion_integration(data, "spareroom")
    except Exception as e:
        print_status(f"Error scraping Spareroom: {e}", 'error')
def test_init():
    print_status("Testing Web Scraper...", 'msg')

    

if __name__ == "__main__":
    print_status("Testing Web Scraper...", 'msg')
    test_spareroom()
    # test_glassdoor()
    # test_rightmove()