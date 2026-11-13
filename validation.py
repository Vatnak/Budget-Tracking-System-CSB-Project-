from datetime import datetime
from decimal import Decimal, InvalidOperation

def validate_expense_id(expense_id, expenses):
    try:
        if isinstance(expense_id, float) and not expense_id.is_integer():
            print("Invalid Expense ID: Please enter a valid integer.")
            return False
        expense_id = int(expense_id)
        
        if expense_id <= 0:
            print ("Invalid Expense ID: Expense ID must be greater than Zero.")
            return False
        if isinstance(expenses, dict):
            duplicate = expense_id in expenses
        else:
            duplicate = any(int(expense.expense_id) == expense_id for expense in expenses)
        if duplicate:
            print("This Expense ID already exists, try again.")
            return False
        return True
    except (ValueError, TypeError):
        print("Invalid Expense ID: Please enter a valid integer.")
        return False

def validate_date(date):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")

        if parsed_date.strftime("%Y-%m-%d") != date:
            print("Invalid Date: Date must follow the YYYY-MM-DD format.")
            return False
        return True
    except (ValueError, TypeError):
        print("Invalid Date: Please enter a valid date in the format YYYY-MM-DD.")
        return False

def validate_category(category):
    if not isinstance(category, str) or not category.strip():
        print("Invalid Category: Please enter a valid category.")
        return False
    return True

def validate_amount(amount):
    try:
        value = Decimal(str(amount))

        if not value.is_finite() or value <= 0:
            print("Invalid Amount: Amount must be greater than zero")
            return False
        return True

    except (InvalidOperation, ValueError, TypeError):
        print("Invalid Amount: Please enter a valid amount.")
        return False

def validate_note(note):
    if not isinstance(note, str) or not note.strip():
        print("Invalid Note: Please enter a valid note.")
        return False
    return True

#Validate the expense entries
def validate_expense(expense, expenses):
    is_valid = True

    if not validate_expense_id(expense.expense_id, expenses):
        is_valid = False
    if not validate_date(expense.date):
        is_valid = False
    if not validate_category(expense.category):
        is_valid = False
    if not validate_amount(expense.amount):
        is_valid = False
    if not validate_note(expense.note):
        is_valid = False

    return is_valid

#Validate expense update entries
def validate_expense_update(expense):
    is_valid = True

    if not validate_date(expense.date):
        is_valid = False
    if not validate_category(expense.category):
        is_valid = False
    if not validate_amount(expense.amount):
        is_valid = False
    if not validate_note(expense.note):
        is_valid = False

    return is_valid
