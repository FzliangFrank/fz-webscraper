from .scrapers.glassdoor import GlassdoorScraper
from .scrapers.rightmove import RightmoveScraper
from .scrapers.spareroom import SpareRoomScraper
from .config import load_config
import os
import re

def identify_site(url: str) -> str:
    """
    Identify the site type based on the URL.
    """
    site = re.findall(r'https?://(?:www\.)?([^/]+)', url)[0]
    match site:
        case 'glassdoor':
            return 'glassdoor'
        case 'rightmove.co.uk':
            return 'rightmove'
        case 'spareroom.co.uk':
            return 'spareroom'
        case _:
            raise ValueError(f"Unsupported site: {site}. Supported types are 'glassdoor' and 'rightmove'")

def scrape_url(url: str, site_type: str = None) -> dict:
    """
    Scrape data from a given URL based on the site type.
    
    Args:
        url (str): The URL to scrape
        site_type (str): Type of site ('glassdoor' or 'rightmove')
        
    Returns:
        dict: Scraped data in key-value pairs
    """
    config = load_config()
    if site_type is None:
        site_type = identify_site(url)
    
    if site_type.lower() == 'glassdoor':
        scraper = GlassdoorScraper(config['glassdoor'])
        return scraper.scrape(url)
    elif site_type.lower() == 'rightmove':
        scraper = RightmoveScraper(config['rightmove'])
        return scraper.scrape(url)
    elif site_type.lower() == 'spareroom':
        scraper = SpareRoomScraper(config['spareroom'])
        return scraper.scrape(url)
    else:
        raise ValueError(f"Unsupported site type: {site_type}. Supported types are 'glassdoor' and 'rightmove'") 