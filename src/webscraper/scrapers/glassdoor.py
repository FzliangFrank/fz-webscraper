from typing import Dict, Any
from .base import BaseScraper

class GlassdoorScraper(BaseScraper):
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape job listing data from Glassdoor.
        Extends parent scrape method with additional custom extraction logic.
        
        Args:
            url (str): Glassdoor job listing URL
            
        Returns:
            Dict[str, Any]: Job listing data
        """
        # First get data using parent's scrape method
        data = super().scrape(url)
        
        # Get the soup object again for custom extraction if needed
        soup = self._get_page(url)
        
        # Add any Glassdoor-specific custom extraction logic here
        # For example:
        # if 'reviews_count' in data and not data['reviews_count']:
        #     try:
        #         reviews_element = soup.find('div', class_='reviews-count')
        #         if reviews_element:
        #             data['reviews_count'] = reviews_element.text.strip()
        #     except (AttributeError, TypeError):
        #         pass
        
        return data

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the scraped Glassdoor data.
        Add any Glassdoor-specific data processing here.
        
        Args:
            data (Dict[str, Any]): Raw scraped data
            
        Returns:
            Dict[str, Any]: Processed data
        """
        # Clean up salary data if it exists
        if data.get('salary'):
            # Remove any "Estimated:" prefix and clean up the format
            data['salary'] = data['salary'].replace('Estimated:', '').strip()
            
            # Try to extract numeric values from salary range
            try:
                salary_text = data['salary'].replace('$', '').replace(',', '')
                if '-' in salary_text:
                    min_salary, max_salary = salary_text.split('-')
                    data['salary_min'] = float(min_salary.replace('K', '000').strip())
                    data['salary_max'] = float(max_salary.replace('K', '000').strip())
            except (ValueError, AttributeError):
                # If salary parsing fails, keep the original text
                pass
        
        # Clean up location data
        if data.get('location'):
            # Split location into city and state if possible
            try:
                city, state = data['location'].split(',')
                data['city'] = city.strip()
                data['state'] = state.strip()
            except ValueError:
                # If splitting fails, keep the original location
                pass
        
        return data 