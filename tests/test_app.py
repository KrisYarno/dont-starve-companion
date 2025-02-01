import unittest
from models import get_engine, create_tables, get_session, Item, Character
from app import create_app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # Create the app using an in-memory SQLite database.
        self.app = create_app("sqlite:///:memory:")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        
        # Get the session from the app's config.
        self.session = self.app.config["DB_SESSION"]
        
        # Add a test item.
        test_item = Item(name="Test Item", ingredients="Wood, Stone", obtaining_method="Crafting")
        self.session.add(test_item)
        self.session.commit()
        
        # Add a test character.
        test_character = Character(name="Wolfgang", perks="Combat boost", description="Strong and fearless")
        self.session.add(test_character)
        self.session.commit()
    
    def test_get_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(isinstance(data, list))
        self.assertGreaterEqual(len(data), 1)
    
    def test_get_item(self):
        response = self.client.get("/items/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Test Item")
    
    def test_get_characters(self):
        response = self.client.get("/characters")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(isinstance(data, list))
        self.assertGreaterEqual(len(data), 1)
    
    def test_compare_characters(self):
        # Assuming the test character gets ID 1.
        response = self.client.get("/characters/compare?ids=1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Wolfgang", data)

if __name__ == "__main__":
    unittest.main()
