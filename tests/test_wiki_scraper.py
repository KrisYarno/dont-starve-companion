import unittest
from wiki_scraper import WikiScraper
from bs4 import BeautifulSoup

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
    def json(self):
        return self._json
    def raise_for_status(self):
        pass

class DummySession:
    def __init__(self, html_content):
        self.html_content = html_content
    def get(self, url, params=None):
        # Return a dummy response with the provided HTML content when parsing.
        if params.get("action") == "parse":
            return DummyResponse({
                "parse": {
                    "text": {"*": self.html_content}
                }
            })
        return DummyResponse({})

class TestWikiScraper(unittest.TestCase):
    def test_fetch_item_details(self):
        # Dummy HTML simulating an item page with an infobox.
        dummy_html = '''
        <html>
        <body>
            <table class="infobox">
                <tr>
                    <th>Ingredients</th>
                    <td>Wood, Stone, Gold</td>
                </tr>
                <tr>
                    <th>Obtained From</th>
                    <td>Crafting, Mining</td>
                </tr>
            </table>
        </body>
        </html>
        '''
        scraper = WikiScraper()
        scraper.session = DummySession(dummy_html)
        details = scraper.fetch_item_details("Test Item")
        self.assertEqual(details["name"], "Test Item")
        self.assertEqual(details["ingredients"], "Wood, Stone, Gold")
        self.assertEqual(details["obtaining_method"], "Crafting, Mining")

if __name__ == "__main__":
    unittest.main()
