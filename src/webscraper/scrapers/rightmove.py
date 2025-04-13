from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
from .base import BaseScraper
import re

class RightmoveScraper(BaseScraper):
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape property listing data from Rightmove.
        
        Args:
            url (str): Rightmove property listing URL
            
        Returns:
            Dict[str, Any]: Property listing data
        """
        data = super().scrape(url)
        return data

    def _extract_bedrooms(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract number of bedrooms from the page."""
        try:
            # Find span containing 'bed', then navigate up to parent container
            bed_span = soup.find('span', string=lambda x: x and 'bed' in x.lower())
            if bed_span:
                bed_parent = bed_span.parent.parent
                # Find the span with just the number within this parent
                bed_number = bed_parent.find('span', string=lambda x: x and re.match(r'^\d+$', str(x).strip()))
                if bed_number:
                    return bed_number.text.strip()
        except (AttributeError, TypeError) as e:
            print(f"Error extracting bedrooms: {e}")
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract property description from the page."""
        try:
            description_parent = soup.find('h2', string=lambda x: x and re.search(r'description', str(x).lower()))
            if description_parent:
                description_div = description_parent.parent.find('div')
                if description_div:
                    return description_div.text.strip()
        except (AttributeError, TypeError) as e:
            print(f"Error extracting description: {e}")
        return None

    def _extract_deposit(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract deposit amount from the page."""
        try:
            deposit_parent = soup.find('dt', string=lambda x: x and re.search(r'deposit', str(x).lower()))
            if deposit_parent:
                deposit_dd = deposit_parent.parent.find('dd')
                if deposit_dd:
                    deposit_text = deposit_dd.text.strip()
                    deposit_match = re.search(r'£([\d,]+)', deposit_text)
                    if deposit_match:
                        return deposit_match.group(1)
        except (AttributeError, TypeError) as e:
            print(f"Error extracting deposit: {e}")
        return None

    def _extract_images(self, soup: BeautifulSoup) -> list[str]:
        """Extract all image URLs from the page."""
        images = soup.find_all('img', {'data-object-fit': 'cover'})
        images_url = [img['src'] for img in images]
        return images_url

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the scraped Rightmove data.
        Add any Rightmove-specific data processing here.
        
        Args:
            data (Dict[str, Any]): Raw scraped data
            
        Returns:
            Dict[str, Any]: Processed data
        """
        # Process price data
        if data.get('price'):
            try:
                price_str = data['price'].replace('£', '').replace(',', '')
                
                if 'pcm' in price_str.lower():
                    price_str = price_str.lower().replace('pcm', '').strip()
                    data['price_value'] = float(price_str)
                    data['price_frequency'] = 'monthly'
                else:
                    data['price_value'] = float(price_str)
                    data['price_frequency'] = 'one-time'
            except ValueError:
                data['price_value'] = None
                data['price_frequency'] = None
        
        # Process bedrooms data
        if data.get('bedrooms'):
            try:
                data['bedrooms'] = int(data['bedrooms'])
            except ValueError:
                print(f"Error processing bedrooms: {data['bedrooms']}")
                pass

        # Process deposit data
        if data.get('deposit'):
            try:
                data['deposit_value'] = float(data['deposit'].replace(',', ''))
            except (ValueError, TypeError):
                pass

        # Set title if not present
        if not data.get('title'):
            data['title'] = data.get('address', '')
        
        return data
