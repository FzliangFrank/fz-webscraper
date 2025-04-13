"""
Notion integration module for storing web scraper data in a Notion database.
"""
import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
import toml
from notion_client import Client

class NotionManager:
    def __init__(self, site_type: str = None):
        """
        Initialize the Notion manager with field mapping configuration.
        
        Args:
            site_type (str): Type of site being scraped ('rightmove' or 'glassdoor')
        """
        load_dotenv()
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        
        # Load mapping configuration from the config directory
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 'config', 'notion_mapping.toml')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Notion mapping configuration file not found at {config_path}\n"
                "Please ensure you have config/notion_mapping.toml in your project root."
            )
            
        self.config = toml.load(config_path)
        
        # Set field mappings based on site type
        self.field_mapping = self.config.get(site_type, {}) if site_type else {}
        self.field_types = self.config.get('field_types', {})

    def create_image_blocks(self, image_urls: List[str]) -> List[Dict]:
        """
        Create Notion blocks for embedding images.
        
        Args:
            image_urls (List[str]): List of image URLs to embed
            
        Returns:
            List[Dict]: List of Notion block objects for images
        """
        image_blocks = []
        for url in image_urls:
            image_blocks.append({
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": url
                    }
                }
            })
        return image_blocks

    def convert_value(self, field_name: str, value: Any) -> Any:
        """
        Convert value based on field type configuration.
        
        Args:
            field_name (str): Name of the field being converted
            value (Any): Value to convert
            
        Returns:
            Any: Converted value
        """
        if not value:
            return value
            
        field_type = self.field_types.get(field_name)
        
        if field_type == "number" and isinstance(value, str):
            try:
                # Extract numeric characters and convert to number
                numeric = ''.join(filter(str.isdigit, value))
                return int(numeric) if numeric else None
            except (ValueError, TypeError):
                print(f"Warning: Could not convert value '{value}' to number")
                return None
                
        return value
        
    def map_data_to_notion_properties(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map the scraper data to Notion database properties based on field mapping.
        
        Args:
            data (Dict[str, Any]): The scraped data dictionary
            
        Returns:
            Dict[str, Any]: Mapped Notion properties
        """
        properties = {}
        for scraper_key, notion_field in self.field_mapping.items():
            if scraper_key in data:
                # Get and convert value based on field type
                value = self.convert_value(scraper_key, data[scraper_key])
                if value is None:
                    continue
                    
                # Map to Notion property format
                field_type = self.field_types.get(scraper_key)
                
                if field_type == "title":
                    properties[notion_field] = {"title": [{"text": {"content": str(value)}}]}
                elif field_type == "url" and isinstance(value, str):
                    properties[notion_field] = {"url": value}
                elif isinstance(value, str):
                    properties[notion_field] = {"rich_text": [{"text": {"content": value}}]}
                elif isinstance(value, (int, float)):
                    properties[notion_field] = {"number": value}
                elif isinstance(value, bool):
                    properties[notion_field] = {"checkbox": value}
        
        return properties
    
    def add_entry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new entry to the Notion database with images if available.
        
        Args:
            data (Dict[str, Any]): The scraped data dictionary
            
        Returns:
            Dict[str, Any]: The created Notion page
        """
        # Ensure we have the original URL in the data
        if "url" not in data:
            data["url"] = data.get("source_url", "")  # Fallback to source_url if available
            
        properties = self.map_data_to_notion_properties(data)
        
        # Create the page first
        page = self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
        
        # If there are images, add them to the page
        if "images" in data and data["images"]:
            image_blocks = self.create_image_blocks(data["images"])
            
            # Add images to the page content
            self.notion.blocks.children.append(
                block_id=page["id"],
                children=image_blocks
            )
        
        return page

# Example usage:
# field_mapping = {
#     "title": "Name",           # Maps scraper's "title" to Notion's "Name" field
#     "price": "Price",          # Maps scraper's "price" to Notion's "Price" field
#     "location": "Location",    # Maps scraper's "location" to Notion's "Location" field
#     "description": "Details"   # Maps scraper's "description" to Notion's "Details" field
# }
# notion_manager = NotionManager(field_mapping)
# notion_manager.add_entry(scraped_data) 