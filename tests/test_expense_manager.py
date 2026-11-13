import json
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from decimal import Decimal
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from expense import Expense
from expense_manager import ExpenseManager
from main import add_expense, delete_expense, save_changes, update_expense
from storage import load_expenses, save_expenses
from summary import calculate_category_totals, calculate_total_expenses


class ExpenseManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = ExpenseManager()
        self.food = Expense(10, "2026-11-13", "Food", 5.5, "Lunch")
        self.transport = Expense(42, "2026-11-12", "Transport", 2.0, "Bus")
        self.manager.add_expense(self.food)
        self.manager.add_expense(self.transport)

    def test_lookup_uses_id_and_duplicates_do_not_replace_records(self):
        self.assertIs(self.manager.get_expense(42), self.transport)
        self.assertIsNone(self.manager.get_expense(1))
        with redirect_stdout(StringIO()):
            self.assertFalse(self.manager.add_expense(
                Expense("42", "2026-11-13", "Food", 9, "Duplicate")))
        self.assertIs(self.manager.get_expense(42), self.transport)
        self.assertTrue(self.manager.add_expense(
            Expense("50", "2026-11-13", "Food", 9, "Dinner")))
        self.assertEqual(self.manager.get_expense(50).expense_id, 50)

    def test_update_validation_and_delete_by_id(self):
        self.assertTrue(self.manager.update_expense(42, amount=3.5))
        self.assertEqual(self.transport.amount, 3.5)
        with redirect_stdout(StringIO()):
            self.assertFalse(self.manager.update_expense(42, amount=-1))
        self.assertEqual(self.transport.amount, 3.5)
        self.assertFalse(self.manager.update_expense(1, amount=1))
        self.assertTrue(self.manager.delete_expense(10))
        self.assertIsNone(self.manager.get_expense(10))
        self.assertFalse(self.manager.delete_expense(10))
        self.assertEqual(self.manager.view_expense(), [self.transport])

    def test_filtering_and_summaries_use_expense_objects(self):
        self.assertEqual(self.manager.search_expense(category="Food"), [self.food])
        self.assertEqual(self.manager.search_expense(date="2026-11-12"), [self.transport])
        self.assertEqual(self.manager.search_expense(category="Food", date="2026-11-12"), [])
        self.assertEqual(calculate_total_expenses(self.manager.view_expense()), Decimal("7.5"))
        self.assertEqual(calculate_category_totals(self.manager.view_expense()),
                         {"Food": Decimal("5.5"), "Transport": Decimal("2.0")})

    def test_json_round_trip_preserves_list_format(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "expenses.json"
            with redirect_stdout(StringIO()):
                save_changes(self.manager, {}, filename)
            records = json.loads(filename.read_text(encoding="utf-8"))
            self.assertEqual(records, [self.food.to_dict(), self.transport.to_dict()])
            restored = ExpenseManager()
            for expense in load_expenses(filename):
                self.assertTrue(restored.add_expense(expense))
            self.assertEqual(restored.get_expense(42).to_dict(), self.transport.to_dict())
            self.assertTrue(restored.delete_expense(10))
            self.assertTrue(restored.delete_expense(42))
            self.assertTrue(save_expenses(restored.view_expense(), filename))
            self.assertEqual(json.loads(filename.read_text(encoding="utf-8")), [])

    def test_failed_save_restores_dictionary_and_previous_values(self):
        previous = deepcopy(self.manager.expenses)
        self.manager.update_expense(42, amount=99)
        with patch("main.save_expenses", return_value=False), redirect_stdout(StringIO()):
            save_changes(self.manager, previous, "unused.json")
        self.assertEqual(self.manager.get_expense(42).amount, 2.0)
        self.assertTrue(self.manager.delete_expense(10))

    def test_cli_add_update_delete_integrate_with_dictionary(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(StringIO()):
            filename = Path(directory) / "expenses.json"
            with patch("builtins.input", side_effect=["2026-11-13", "Food", "4", "Snack"]):
                add_expense(self.manager, filename)
            self.assertEqual(self.manager.get_expense(43).note, "Snack")
            with patch("builtins.input", side_effect=["43", "", "", "6", ""]):
                update_expense(self.manager, filename)
            self.assertEqual(self.manager.get_expense(43).amount, 6)
            with patch("builtins.input", side_effect=["43", "yes"]):
                delete_expense(self.manager, filename)
            self.assertIsNone(self.manager.get_expense(43))
            self.assertEqual([expense.expense_id for expense in load_expenses(filename)], [10, 42])


if __name__ == "__main__":
    unittest.main()
