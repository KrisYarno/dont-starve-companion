import requests
from bs4 import BeautifulSoup
import logging

class WikiScraper:
    """
    A class to scrape the Don't Starve Together Wiki for item and character data.
    """
    def __init__(self):
        self.base_api_url = "https://dontstarve.fandom.com/api.php"
        self.session = requests.Session()
    
    def fetch_item_list(self, category="Category:Items", limit=500):
        """
        Fetch the list of item titles from the given category using the MediaWiki API.
        """
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": limit,
            "format": "json"
        }
        response = self.session.get(self.base_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("query", {}).get("categorymembers", [])
        return items
    
    def fetch_item_details(self, title):
        """
        Fetch the details for an item by its title.
        """
        params = {
            "action": "parse",
            "page": title,
            "prop": "text",
            "format": "json"
        }
        response = self.session.get(self.base_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        html_content = data.get("parse", {}).get("text", {}).get("*", "")
        if not html_content:
            logging.warning(f"No content found for item: {title}")
            return None
        
        soup = BeautifulSoup(html_content, "html.parser")
        item_data = {"name": title, "ingredients": None, "obtaining_method": None}
        infobox = soup.find("table", class_="infobox")
        if infobox:
            for row in infobox.find_all("tr"):
                header = row.find("th")
                value = row.find("td")
                if header and value:
                    header_text = header.get_text().strip().lower()
                    if "ingredient" in header_text:
                        item_data["ingredients"] = value.get_text(separator=", ").strip()
                    elif "obtain" in header_text or "gather" in header_text:
                        item_data["obtaining_method"] = value.get_text(separator=", ").strip()
        return item_data

    # New method: Fetch list of characters.
    def fetch_character_list(self, category="Category:Characters", limit=100):
        """
        Fetch the list of character titles from the given category using the MediaWiki API.
        """
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": limit,
            "format": "json"
        }
        response = self.session.get(self.base_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        characters = data.get("query", {}).get("categorymembers", [])
        return characters

    # New method: Fetch character details.
    def fetch_character_details(self, title):
        """
        Fetch the details for a character by its title.
        Returns a dictionary with keys: 'name', 'perks', and 'description'.
        """
        params = {
            "action": "parse",
            "page": title,
            "prop": "text",
            "format": "json"
        }
        response = self.session.get(self.base_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        html_content = data.get("parse", {}).get("text", {}).get("*", "")
        if not html_content:
            logging.warning(f"No content found for character: {title}")
            return None
        
        soup = BeautifulSoup(html_content, "html.parser")
        character_data = {"name": title, "perks": None, "description": None}
        # Look for an infobox that might contain perks/abilities.
        infobox = soup.find("table", class_="infobox")
        if infobox:
            for row in infobox.find_all("tr"):
                header = row.find("th")
                value = row.find("td")
                if header and value:
                    header_text = header.get_text().strip().lower()
                    if "perk" in header_text or "ability" in header_text:
                        character_data["perks"] = value.get_text(separator=", ").strip()
        # Optionally, extract a description from the first paragraph.
        paragraph = soup.find("p")
        if paragraph:
            character_data["description"] = paragraph.get_text().strip()
        return character_data
