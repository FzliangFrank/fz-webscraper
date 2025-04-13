# Web Scraper with Notion Integration

A Python package for scraping property listings from Rightmove, SpareRoom, and job listings from Glassdoor, with automatic upload to Notion databases.

## Installation

```bash
# Install from the current directory
pip install .
```

## Configuration

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Add your Notion API key and database ID to `.env`:
```
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_database_id_here
```

3. Share your Notion database with the integration
4. Configure field mappings in `config/notion_mapping.toml` if needed

## Command Line Usage

After installation, you can use the `webscraper` command:

```bash
# Basic usage
webscraper <URL> <type>

# Example for Rightmove
webscraper "https://www.rightmove.co.uk/properties/123456789" rightmove

# Example for SpareRoom
webscraper "https://www.spareroom.co.uk/flatshare/123456" spareroom

# Example for Glassdoor
webscraper "https://www.glassdoor.co.uk/job-listing/123456789" glassdoor

# Options:
#  -d, --debug        Print debug information including scraped data
#  -s, --skip-notion  Skip Notion upload and just print scraped data
```

### Examples

1. Scrape and upload to Notion:
```bash
webscraper "https://www.rightmove.co.uk/properties/123456789" rightmove
webscraper "https://www.spareroom.co.uk/flatshare/123456" spareroom
```

2. Scrape with debug output:
```bash
webscraper "https://www.rightmove.co.uk/properties/123456789" rightmove -d
```

3. Scrape without uploading to Notion:
```bash
webscraper "https://www.rightmove.co.uk/properties/123456789" rightmove -s
```

## Python Usage

You can also use the package in your Python code:

```python
from webscraper import scrape_url
from webscraper.notion_client import NotionManager

# Scrape data
data = scrape_url("https://www.rightmove.co.uk/properties/123456789", "rightmove")
# or
data = scrape_url("https://www.spareroom.co.uk/flatshare/123456", "spareroom")

# Upload to Notion
notion = NotionManager("rightmove")  # or "spareroom"
result = notion.add_entry(data)
```

## Supported Websites

- Rightmove (property listings)
- SpareRoom (property listings)
- Glassdoor (job listings)

## Features

- Scrapes detailed information from supported websites
- Automatic type conversion for Notion fields
- Configurable field mappings via TOML
- Supports embedding images in Notion pages
- Command-line interface for easy use
- Debug mode for troubleshooting
- Color-coded console output
- Custom extractor methods for complex data fields

## Environment Setup

### Using Conda (Recommended)
```bash
# Create and activate the conda environment
conda env create -f environment.yml
conda activate webscraper
```

### Using pip
```bash
pip install .
```

## Configuration

The scraping configurations are split into two files:

1. `config/scrapers.toml` - Contains website-specific selectors and patterns:
```toml
[rightmove]
type = "property_listing"
extractors.price = { type = "pattern", pattern = "£[\\d,]+(?:\\s*pcm)?", tag = "span" }
extractors.description = { type = "*" }  # Uses custom extractor method
# ... more extractors

[spareroom]
type = "property_listing"
extractors.price = { type = "pattern", tag = "dt", pattern = "£[\\d,]+(?:\\s*pcm)?" }
extractors.address = { type = "*" }  # Uses custom extractor method
# ... more extractors
```

2. `config/notion_mapping.toml` - Maps scraped fields to Notion database columns:
```toml
[rightmove]
price_value = "Price (pcm)"
address = "Address"
description = "Description"
# ... more mappings

[spareroom]
price_value = "Price (pcm)"
address = "Address"
description = "Description"
# ... more mappings
```

Fields marked with `type = "*"` in the configuration use custom extractor methods in the scraper classes for complex data extraction.

## Requirements

- Python 3.8+
- beautifulsoup4
- requests
- selenium
- toml
- colorama

All dependencies are automatically installed when using either the conda environment or pip installation methods.

## Note

Please be mindful of the websites' terms of service and robots.txt when using this scraper. Consider implementing appropriate delays between requests and respect rate limits. 