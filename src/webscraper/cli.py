"""
Command-line interface for the web scraper package.
"""
import argparse
import json
from typing import Optional
from colorama import Fore, Style, init
from . import scrape_url, identify_site
from .notion_client import NotionManager

# Initialize colorama for cross-platform colored output
init()

def print_status(message: str, status: str = 'msg') -> None:
    """Print a message with color based on status"""
    if status == 'msg':
        print(Fore.GREEN + message + Style.RESET_ALL)
    elif status == 'warn':
        print(Fore.YELLOW + message + Style.RESET_ALL)
    elif status == 'error':
        print(Fore.RED + message + Style.RESET_ALL)

def scrape_and_upload(url: str, site_type: str=None, debug: bool = False, skip_notion: bool = False) -> Optional[dict]:
    """
    Scrape data from URL and upload to Notion.
    
    Args:
        url (str): URL to scrape
        site_type (str): Type of site ('rightmove' or 'glassdoor')
        debug (bool): Whether to print debug information
        skip_notion (bool): Whether to skip Notion upload and just return data
        
    Returns:
        Optional[dict]: Scraped data if debug is True or skip_notion is True
    """
    if site_type is None:
        try:
            site_type = identify_site(url)
        except ValueError as e:
            print_status(f"Error: {str(e)}", 'error')
            return None
    try:
        # Scrape the URL
        print_status(f"Scraping {site_type} URL: {url}")
        data = scrape_url(url, site_type)
        
        # Add source URL to data
        data["url"] = url
        
        if debug:
            print_status("\nScraped Data:", 'msg')
            print(json.dumps(data, indent=2))
            
        if not skip_notion:
            # Upload to Notion
            print_status("\nUploading to Notion...")
            notion = NotionManager(site_type)
            result = notion.add_entry(data)
            print_status(f"Successfully added to Notion! Page ID: {result['id']}")
            
        return data if debug or skip_notion else None
        
    except Exception as e:
        print_status(f"Error: {str(e)}", 'error')
        return None

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape data from supported websites and upload to Notion"
    )
    
    parser.add_argument(
        "url",
        help="URL to scrape"
    )
    
    parser.add_argument(
        "--type",
        choices=["rightmove", "glassdoor", "spareroom"],
        help="Type of website to scrape",
        required=False
    )
    
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Print debug information including scraped data"
    )
    
    parser.add_argument(
        "-s", "--skip-notion",
        action="store_true",
        help="Skip Notion upload and just print scraped data"
    )
    
    args = parser.parse_args()
    
    scrape_and_upload(args.url, args.type, args.debug, args.skip_notion)

if __name__ == "__main__":
    main() 