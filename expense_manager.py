from expense import Expense

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def view_expense(self):
        return self.expenses

    def search_expense(self, category):
        result = []

        for expense in self.expenses:
            if expense.category == category:
                result.append(expense)
        return result

    def update_expense(self, expense_id, amount):
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                expense.amount = amount
                return True

        return False

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                self.expenses.remove(expense)
                return True 
        return False
