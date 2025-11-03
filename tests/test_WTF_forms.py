import unittest
from app import app

class LoginFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # Вимикаємо CSRF для тестів
        self.client = app.test_client()

    def test_login_get(self):
        """Перевірка завантаження сторінки логіну."""
        response = self.client.get("/login")
        html = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вхід", html)

    def test_login_valid_credentials(self):
        """Перевірка успішного входу."""
        response = self.client.post(
            "/login",
            data={"user": "jar", "password": "1234", "remember": "y"},
            follow_redirects=True
        )
        html = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вітаємо, jar", html)
        self.assertIn("Запам", html)

    def test_login_invalid_credentials(self):
        """Перевірка входу з неправильними даними."""
        response = self.client.post(
            "/login",
            data={"user": "bad", "password": "wrong"},
            follow_redirects=True
        )
        html = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Невірні дані", html)

    def test_login_validation(self):
        """Перевірка валідації форми (замалий пароль)."""
        response = self.client.post(
            "/login",
            data={"user": "jar", "password": "123"},
            follow_redirects=True
        )
        html = response.data.decode("utf-8")
        self.assertIn("Довжина паролю", html)

class ContactFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_contacts_get(self):
        """Перевірка завантаження сторінки контактів."""
        response = self.client.get("/contacts")
        html = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Повідомлення", html)

    def test_contacts_valid_submission(self):
        """Перевірка успішного відправлення контактної форми."""
        response = self.client.post(
            "/contacts",
            data={
                "name": "Yaro",
                "email": "test@example.com",
                "phone": "+380931234567",
                "subject": "feedback",
                "message": "Все чудово!"
            },
            follow_redirects=True
        )
        html = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ваше повідомлення успішно надіслано", html)

    def test_contacts_invalid_email(self):
        """Перевірка валідації email."""
        response = self.client.post(
            "/contacts",
            data={
                "name": "Yaro",
                "email": "wrongemail",
                "phone": "+380931234567",
                "subject": "feedback",
                "message": "Тест"
            },
            follow_redirects=True
        )
        html = response.data.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Некоректний email", html)

    def test_contacts_invalid_phone(self):
        """Перевірка формату телефону."""
        response = self.client.post(
            "/contacts",
            data={
                "name": "Yaro",
                "email": "test@example.com",
                "phone": "12345",
                "subject": "support",
                "message": "Test"
            },
            follow_redirects=True
        )
        html = response.data.decode("utf-8")
        self.assertIn("Формат телефону", html)

if __name__ == "__main__":
    unittest.main()