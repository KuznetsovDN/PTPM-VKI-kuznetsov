import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        # Каждый тест — чистая БД в памяти
        self.db = DatabaseRepository(":memory:")

    # ================= get_by_id (2 теста) =================
    def test_get_by_id_existing(self):
        self.db.add(1, "alice", "<p>hi</p>")
        row = self.db.get_by_id(1)
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "alice")
        self.assertEqual(row["message"], "<p>hi</p>")

    def test_get_by_id_missing(self):
        self.assertIsNone(self.db.get_by_id(999))

    # ================= get_by_name (2 теста) =================
    def test_get_by_name_returns_list(self):
        self.db.add(1, "alice", "a1")
        self.db.add(2, "alice", "a2")
        self.db.add(3, "bob", "b1")
        rows = self.db.get_by_name("alice")
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["name"] == "alice" for r in rows))

    def test_get_by_name_empty(self):
        self.assertEqual(self.db.get_by_name("nobody"), [])

    # ================= add (2 теста) =================
    def test_add_success(self):
        self.assertTrue(self.db.add(1, "alice", "hello"))
        self.assertIsNotNone(self.db.get_by_id(1))

    def test_add_duplicate_id_raises(self):
        self.db.add(1, "alice", "first")
        with self.assertRaises(ValueError):
            self.db.add(1, "bob", "second")

    def test_add_name_too_long_raises(self):
        with self.assertRaises(ValueError):
            self.db.add(1, "x" * 257, "msg")

    def test_add_message_too_long_raises(self):
        with self.assertRaises(ValueError):
            self.db.add(1, "alice", "x" * 8097)

    def test_add_wrong_type_raises(self):
        with self.assertRaises(ValueError):
            self.db.add("not-int", "alice", "msg")

    # ================= update (2 теста) =================
    def test_update_existing(self):
        self.db.add(1, "alice", "old")
        self.assertTrue(self.db.update(1, "<p>new</p>"))
        self.assertEqual(self.db.get_by_id(1)["message"], "<p>new</p>")

    def test_update_missing_returns_false(self):
        self.assertFalse(self.db.update(999, "new"))

    def test_update_too_long_raises(self):
        self.db.add(1, "alice", "old")
        with self.assertRaises(ValueError):
            self.db.update(1, "x" * 8097)

    # ================= delete (2 теста) =================
    def test_delete_existing(self):
        self.db.add(1, "alice", "msg")
        self.assertTrue(self.db.delete(1))
        self.assertIsNone(self.db.get_by_id(1))

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.db.delete(999))


if __name__ == "__main__":
    unittest.main()