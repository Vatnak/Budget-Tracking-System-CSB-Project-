from expense import Expense
from validation import validate_expense, validate_expense_update

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        if not validate_expense(expense, self.expenses):
            return False

        expense.expense_id = int(expense.expense_id)
        self.expenses.append(expense)
        return True

    def view_expense(self):
        return self.expenses

    def search_expense(self, category=None, date=None):
        result = []

        for expense in self.expenses:
            if category is not None and expense.category != category:
                continue
            if date is not None and expense.date != date:
                continue
            result.append(expense)
        return result

    def update_expense(self, expense_id, amount=None, date=None, category=None, note=None):
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                updated_expense = Expense(
                    expense.expense_id,
                    expense.date if date is None else date,
                    expense.category if category is None else category,
                    expense.amount if amount is None else amount,
                    expense.note if note is None else note
                )

                if not validate_expense_update(updated_expense):
                    return False

                expense.date = updated_expense.date
                expense.category = updated_expense.category
                expense.amount = updated_expense.amount
                expense.note = updated_expense.note
                return True

        return False

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                self.expenses.remove(expense)
                return True 
        return False
