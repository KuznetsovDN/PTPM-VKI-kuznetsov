import os
import unittest
from unittest.mock import Mock, patch

from src.parser import ForumParser
from src.database import DatabaseRepository


FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "page.html")


class TestForumParser(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE, encoding="utf-8") as f:
            self.html = f.read()
        self.parser = ForumParser()

    # ================= test 1: извлечение из фикстуры =================
    def test_parse_html_extracts_all_posts(self):
        posts = self.parser.parse_html(self.html)
        self.assertEqual(len(posts), 3)
        ids = [p["id"] for p in posts]
        self.assertEqual(ids, [101, 102, 103])
        self.assertEqual(posts[0]["name"], "alice")
        self.assertIn("Привет", posts[0]["message"])
        # HTML разметка внутри сохранена
        self.assertIn("<b>мир</b>", posts[0]["message"])

    # ================= test 2: парсинг через requests (mock сети) =================
    def test_parse_page_uses_requests(self):
        fake_response = Mock()
        fake_response.text = self.html
        fake_response.raise_for_status = Mock()

        with patch.object(self.parser.session, "get", return_value=fake_response) as m:
            posts = self.parser.parse_page("http://example.com/thread")
        m.assert_called_once()
        self.assertEqual(len(posts), 3)

    # ================= test 3: сохранение в БД =================
    def test_save_to_db(self):
        posts = self.parser.parse_html(self.html)
        db = DatabaseRepository(":memory:")
        saved = self.parser.save_to_db(posts, db)
        self.assertEqual(saved, 3)
        self.assertIsNotNone(db.get_by_id(101))
        self.assertEqual(len(db.get_by_name("alice")), 2)

    # ================= test 4: пустая страница =================
    def test_parse_empty_html(self):
        self.assertEqual(self.parser.parse_html("<html><body></body></html>"), [])


if __name__ == "__main__":
    unittest.main()