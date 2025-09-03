import json
import yaml
import requests
from bs4 import BeautifulSoup
import os
import time


# A simple class to represent the crawler and its methods
class Crawl4AI:
    """A simple web crawler that extracts data based on a YAML configuration."""

    @staticmethod
    def crawl(config):
        """
        Starts the crawl process for a single site configuration.
        This function now uses the start_urls from the config.
        """
        crawled_data = []
        site_name = config.get("name")
        start_urls = config.get("start_urls", [])
        crawl_depth = config.get("crawl_depth", 1)
        rules = config.get("rules", {})
        mappings = config.get("selector_mappings", {})

        print(f"CRAWL4AI: Starting crawl for '{site_name}'...")
        print(f"  - URLs: {start_urls}")
        print(f"  - Depth: {crawl_depth}")
        print(f"  - Rules: {rules}")
        print(f"  - Mappings: {mappings}")

        # Basic crawling logic to simulate data extraction
        for url in start_urls:
            print(f"  - Fetching URL: {url}")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes

                # Simulate parsing and data extraction from a fictional page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Create a sample data entry based on the mappings
                sample_data = {
                    "source_url": url,
                    "title": "Sample Title Found",
                    "publish_date": "2024-05-20",
                    "author": "Sample Author",
                    "clean_text": "This is a sample of cleaned text from a blog post or article. It simulates the extraction of the main content based on the selector mappings.",
                }
                crawled_data.append(sample_data)

            except requests.exceptions.RequestException as e:
                print(f"    - ERROR: Failed to fetch {url}. Reason: {e}")

            # Simple delay to avoid overwhelming the server
            time.sleep(1)

        print(f"CRAWL4AI: Crawl for '{site_name}' finished.")
        return crawled_data


# Main function to run the crawlers from the config file
def run_crawlers():
    """Reads the YAML configuration and runs the crawler for each enabled site."""
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'crawl_configs.yaml')
    output_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'output_data.json')

    try:
        with open(config_file_path, 'r') as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_file_path}'")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return

    all_crawled_output = []

    # Iterate through each site defined in the YAML file
    sites_config = config_data.get("sites", [])
    if not sites_config:
        print("Warning: No sites found in the configuration file.")
        return

    for site_config in sites_config:
        if site_config.get("enabled", False):
            print(f"\nProcessing configuration for: {site_config.get('name')}")
            crawled_output = Crawl4AI.crawl(site_config)
            all_crawled_output.extend(crawled_output)

    if all_crawled_output:
        print("\nSaving all crawled data to 'output_data.json'...")
        with open(output_file_path, 'w') as f:
            json.dump(all_crawled_output, f, indent=2)
        print("CRAWL4AI: Crawling process complete. Data saved.")
    else:
        print("CRAWL4AI: No data crawled. Skipping file save.")


if __name__ == "__main__":
    run_crawlers()
