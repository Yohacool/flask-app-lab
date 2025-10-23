import unittest
from app import app

class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_page(self):
        """Тест сторінки зі списком продуктів."""
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Mouse", response.data)
        self.assertIn(b"Keyboard", response.data)

if __name__ == "__main__":
    unittest.main()
