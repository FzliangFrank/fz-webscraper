# Web Scraper with Notion Integration

A Python package for scraping property listings from Rightmove and job listings from Glassdoor, with automatic upload to Notion databases.

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

# Upload to Notion
notion = NotionManager("rightmove")
result = notion.add_entry(data)
```

## Supported Websites

- Rightmove (property listings)
- Glassdoor (job listings)

## Features

- Scrapes detailed information from supported websites
- Automatic type conversion for Notion fields
- Configurable field mappings via TOML
- Supports embedding images in Notion pages
- Command-line interface for easy use
- Debug mode for troubleshooting
- Color-coded console output

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

## Usage

```python
from webscraper import scrape_url

# Scrape a Glassdoor job listing
job_data = scrape_url("https://www.glassdoor.com/job-listing/...", "glassdoor")
print(job_data)

# Scrape a Rightmove property listing
property_data = scrape_url("https://www.rightmove.co.uk/properties/...", "rightmove")
print(property_data)
```

## Configuration

The scraping selectors are configured in `config.toml`. You can modify the selectors to match the current HTML structure of the websites:

```toml
[glassdoor]
type = "job_listing"
selectors.job_title = ".job-title"
selectors.company_name = ".employer-name"
# ... more selectors

[rightmove]
type = "property_listing"
selectors.price = ".price-text"
selectors.address = ".address"
# ... more selectors
```

## Requirements

- Python 3.8+
- beautifulsoup4
- requests
- selenium
- toml

All dependencies are automatically installed when using either the conda environment or pip installation methods.

## Note

Please be mindful of the websites' terms of service and robots.txt when using this scraper. Consider implementing appropriate delays between requests and respect rate limits. 