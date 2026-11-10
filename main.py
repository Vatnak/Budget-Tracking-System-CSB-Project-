from copy import deepcopy
from decimal import Decimal
from pathlib import Path

from expense import Expense
from expense_manager import ExpenseManager
from storage import load_expenses, save_expenses
from summary import calculate_total_expenses, calculate_category_totals
from validation import validate_amount, validate_date


def display_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\nID | Date | Category | Amount (USD) | Note")
    print("------------------------------------------------------------")

    for expense in expenses:
        amount = Decimal(str(expense.amount))
        print(f"{expense.expense_id} | {expense.date} | {expense.category} | ${amount:.2f} | {expense.note}")


def read_amount(allow_blank=False):
    while True:
        amount = input("Amount (USD): ").strip()

        if allow_blank and amount == "":
            return None

        try:
            amount = float(amount)
        except ValueError:
            print("Invalid Amount: Please enter a valid amount.")
            continue

        if validate_amount(amount):
            return amount


def read_expense_id():
    try:
        expense_id = int(input("Expense ID: ").strip())
        if expense_id > 0:
            return expense_id
    except ValueError:
        pass

    print("Invalid Expense ID: Please enter a positive integer.")
    return None


def save_changes(manager, previous_expenses, filename):
    if save_expenses(manager.expenses, filename):
        print("Changes saved successfully.")
    else:
        manager.expenses = previous_expenses
        print("The change was cancelled because it could not be saved.")


def add_expense(manager, filename):
    expense_id = 1
    for expense in manager.expenses:
        if expense.expense_id >= expense_id:
            expense_id = expense.expense_id + 1

    date = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    amount = read_amount()
    note = input("Note: ").strip()
    expense = Expense(expense_id, date, category, amount, note)

    previous_expenses = deepcopy(manager.expenses)
    if manager.add_expense(expense):
        save_changes(manager, previous_expenses, filename)


def search_expenses(manager):
    print("Leave a field blank to skip that filter.")
    category = input("Category: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()

    if date and not validate_date(date):
        return

    expenses = manager.search_expense(category=category or None, date=date or None)
    display_expenses(expenses)


def update_expense(manager, filename):
    expense_id = read_expense_id()
    if expense_id is None:
        return

    if not any(expense.expense_id == expense_id for expense in manager.expenses):
        print("Expense ID not found.")
        return

    print("Leave a field blank to keep its current value.")
    date = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    amount = read_amount(allow_blank=True)
    note = input("Note: ").strip()

    previous_expenses = deepcopy(manager.expenses)
    if manager.update_expense(expense_id, amount=amount, date=date or None,
                            category=category or None, note=note or None):
        save_changes(manager, previous_expenses, filename)


def delete_expense(manager, filename):
    expense_id = read_expense_id()
    if expense_id is None:
        return

    if not any(expense.expense_id == expense_id for expense in manager.expenses):
        print("Expense ID not found.")
        return

    confirmation = input("Delete this expense? (yes/no): ").strip().lower()
    if confirmation != "yes":
        print("Deletion cancelled.")
        return

    previous_expenses = deepcopy(manager.expenses)
    if manager.delete_expense(expense_id):
        save_changes(manager, previous_expenses, filename)


def display_summary(expenses):
    total = calculate_total_expenses(expenses)
    print(f"\nTotal spending: ${total:.2f}")
    print("Spending by category:")

    category_totals = calculate_category_totals(expenses)
    if not category_totals:
        print("No expenses found.")

    for category, amount in category_totals.items():
        print(f"{category}: ${amount:.2f}")


def main():
    filename = Path(__file__).with_name("expenses.json")
    manager = ExpenseManager()

    try:
        expenses = load_expenses(filename)
        for expense in expenses:
            if not manager.add_expense(expense):
                print("Unable to load expenses: Please repair the invalid records before continuing.")
                return
    except (ValueError, OSError) as error:
        print(error)
        return

    while True:
        print("\n================================")
        print("      BUDGET TRACKING SYSTEM")
        print("================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search / Filter Expenses")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. View Spending Summary")
        print("7. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(manager, filename)
        elif choice == "2":
            display_expenses(manager.view_expense())
        elif choice == "3":
            search_expenses(manager)
        elif choice == "4":
            update_expense(manager, filename)
        elif choice == "5":
            delete_expense(manager, filename)
        elif choice == "6":
            display_summary(manager.view_expense())
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice: Please enter a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
