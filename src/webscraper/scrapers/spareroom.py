"""
SpareRoom scraper implementation.
"""
from typing import Dict, Any
from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import Optional
import re

class SpareRoomScraper(BaseScraper):
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape property listing data from SpareRoom.
        Extends parent scrape method with additional custom extraction logic.
        
        Args:
            url (str): SpareRoom property listing URL
            
        Returns:
            Dict[str, Any]: Property listing data
        """
        # First get data using parent's scrape method
        data = super().scrape(url)
        
        # Get the soup object again for custom extraction
        soup = self._get_page(url)

        # Custom extraction for description
        if 'description' in data and not data['description']:
            try:
                # Look for description in common SpareRoom locations
                description_element = (
                    soup.find('div', {'class': 'listing-description'}) or
                    soup.find('div', {'id': 'full_description'}) or
                    soup.find('div', string=lambda x: x and 'about this room' in str(x).lower())
                )
                if description_element:
                    data['description'] = description_element.text.strip()
            except (AttributeError, TypeError):
                pass

        # Extract availability dates
        try:
            available_element = soup.find(['div', 'span'], string=lambda x: x and 'available' in str(x).lower())
            if available_element:
                available_text = available_element.text.strip()
                data['availability'] = available_text
        except (AttributeError, TypeError):
            pass

        # Extract bills included info
        try:
            bills_element = soup.find(['div', 'span'], string=lambda x: x and 'bills' in str(x).lower())
            if bills_element:
                bills_text = bills_element.parent.text.strip()
                data['bills_included'] = 'included' in bills_text.lower()
        except (AttributeError, TypeError):
            pass

        
        return data
    
    @staticmethod
    def _extract_deposit(soup: BeautifulSoup) -> Optional[str]:
        """
        Extract deposit information from SpareRoom.
        """
        d = soup.find('dt', string=lambda x: x and 'deposit' in x.lower()).parent.find('dd').text
        return d
    
    @staticmethod
    def _extract_address(soup: BeautifulSoup) -> Optional[str]:
        """
        Extract address information from SpareRoom.
        """
        keyfeature_list = keyfeature_list = soup.find('ul', {'class': 'key-features'}).find_all('li')
        address1 = [ p.text.strip() for p in keyfeature_list][1].strip()
        address3 = [ p.text.strip() for p in keyfeature_list][3].strip()
        full_address = re.sub(r'\s+', ' ', address3 + ', ' + address1)
        return full_address

    @staticmethod
    def _extract_bedrooms(soup: BeautifulSoup) -> Optional[str]:
        """
        Extract bedrooms information from SpareRoom.
        """
        return "1"
    
    @staticmethod
    def _extract_images(soup: BeautifulSoup) -> Optional[str]:
        """
        Extract images information from SpareRoom.
        """
        return [soup.find('img', {'src': True, 'class': 'photo-gallery__main-image'})['src']]

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the scraped SpareRoom data.
        Add any SpareRoom-specific data processing here.
        
        Args:
            data (Dict[str, Any]): Raw scraped data
            
        Returns:
            Dict[str, Any]: Processed data
        """
        # Process price data
        if data.get('price'):
            try:
                # Remove '£' and ',' from price string
                price_str = data['price'].replace('£', '').replace(',', '')
                
                # Handle different price frequencies
                price_str = price_str.lower()
                if 'pw' in price_str or 'per week' in price_str:
                    price_str = re.sub(r'pw|per week', '', price_str).strip()
                    data['price_value'] = float(price_str)
                    data['price_frequency'] = 'weekly'
                elif 'pcm' in price_str or 'per month' in price_str:
                    price_str = re.sub(r'pcm|per month', '', price_str).strip()
                    data['price_value'] = float(price_str)
                    data['price_frequency'] = 'monthly'
                else:
                    data['price_value'] = float(price_str)
                    data['price_frequency'] = 'monthly'  # Default to monthly
            except ValueError:
                data['price_value'] = None
                data['price_frequency'] = None
        
        # Process bedrooms data
        if data.get('bedrooms'):
            try:
                data['bedrooms'] = int(data['bedrooms'])
            except ValueError:
                raise ValueError(f"Error processing bedrooms: {data['bedrooms']}")
        
        # Process deposit if present
        if data.get('deposit'):
            try:
                deposit_str = data['deposit'].replace('£', '').replace(',', '')
                data['deposit_value'] = float(deposit_str)
            except ValueError:
                pass

        # Generate title if not present
        if not data.get('title'):
            title_parts = []
            if data.get('bedrooms'):
                title_parts.append(f"{data['bedrooms']} Bedroom")
            if data.get('property_type'):
                title_parts.append(data['property_type'])
            if data.get('address'):
                title_parts.append(f"in {data['address']}")
            
            data['title'] = " ".join(title_parts) if title_parts else data.get('address', 'Room to Rent')
        if len(data.get('description')) > 2000:
            data['description'] = data['description'][:1500] + '...'
        return data