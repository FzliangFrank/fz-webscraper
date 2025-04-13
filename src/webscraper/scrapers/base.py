from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
import requests
from bs4 import BeautifulSoup
import re
import toml

class BaseScraper(ABC):
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the scraper with configuration.
        
        Args:
            config (Dict[str, Any], optional): Configuration dictionary for the scraper.
                                             If None, will load from config file.
        """
        if config is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'config',
                'scrapers.toml'
            )
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Scraper configuration file not found at {config_path}")
            
            all_config = toml.load(config_path)
            # Get the config section for this scraper type
            scraper_type = self.__class__.__name__.lower().replace('scraper', '')
            config = all_config.get(scraper_type, {})
            
        self.config = config
        self.extractors = config.get('extractors', {})
    
    def _get_page(self, url: str) -> BeautifulSoup:
        """
        Get the page content and return a BeautifulSoup object.
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup: Parsed HTML content
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self.url = url
        return BeautifulSoup(response.text, 'html.parser')
    
    def _extract_with_css(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """
        Extract data using CSS selector.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            selector (str): CSS selector
            
        Returns:
            Optional[str]: Extracted text if found, None otherwise
        """
        element = soup.select_one(selector)
        return element.text.strip() if element else None
    
    def _extract_with_pattern(self, soup: BeautifulSoup, pattern: str, tag: str, extract_pattern: Optional[str] = None) -> Optional[str]:
        """
        Extract data using regex pattern search.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            pattern (str): Regex pattern to search for
            tag (str): HTML tag to search in
            extract_pattern (Optional[str]): Pattern to extract specific part of the match
            
        Returns:
            Optional[str]: Extracted text if found, None otherwise
        """
        element = soup.find(tag, string=lambda x: x and re.search(pattern, str(x)))
        if not element:
            return None
            
        text = element.text.strip()
        if extract_pattern:
            match = re.search(extract_pattern, text)
            return match.group(0) if match else None
        return text
    def _extract_wildcard(self, soup: BeautifulSoup, field: str) -> Optional[str]:
        """
        Extract data using custom function.
        """
        if getattr(self, f'_extract_{field}', None):
            try:
                rs = getattr(self, f'_extract_{field}')(soup)
                return rs
            except Exception as e:
                raise ValueError(f"Error extracting {field}: {e} (please check the custom extractor)")
        else:
            raise ValueError(f"No custom extractor (self._extract_{field}) for field: {field}")
    def _extract_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract data from BeautifulSoup object using configured extractors.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            
        Returns:
            Dict[str, str]: Extracted data as key-value pairs
        """
        data = {}
        data['url'] = self.url
        for field, extractor in self.extractors.items():
            match extractor['type']:
                case 'css':
                    data[field] = self._extract_with_css(soup, extractor['selector'])
                case 'pattern':
                    data[field] = self._extract_with_pattern(
                        soup,
                        extractor['pattern'],
                        extractor['tag'],
                        extractor.get('extract')
                    )
                case '*':
                    data[field] = self._extract_wildcard(soup, field)
                case _:
                    raise ValueError(f"Unsupported extractor type: {extractor['type']}")
        return data
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape data from the given URL using configured extractors.
        
        Args:
            url (str): URL to scrape
            
        Returns:
            Dict[str, Any]: Scraped data
        """
        soup = self._get_page(url)
        data = self._extract_data(soup)
        return self.process_data(data)
    
    @abstractmethod
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the extracted data before returning.
        Child classes can override this to add custom processing.
        
        Args:
            data (Dict[str, Any]): Raw extracted data
            
        Returns:
            Dict[str, Any]: Processed data
        """
        return data 