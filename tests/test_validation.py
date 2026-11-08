# from validation import validate_expense_id, validate_date, validate_category, validate_amount, validate_note

# class TestExpense:
#     def __init__(self, expense_id):
#         self.expense_id = expense_id

# expenses = [TestExpense(1), TestExpense(2), TestExpense(3)]

# print(validate_expense_id(4, expenses))
# print(validate_expense_id(1, expenses))
# print(validate_expense_id(0, expenses))
# print(validate_expense_id(-5, expenses))
# print(validate_expense_id("hello", expenses))
# print(validate_expense_id(2.5, expenses))

# from validation import validate_category

# print(validate_category("Food"))
# print(validate_category("Transportation"))
# print(validate_category(""))
# print(validate_category("   "))
# print(validate_category(123))
# print(validate_category(None))

# from validation import validate_amount

# print(validate_amount(25.50))
# print(validate_amount("100"))
# print(validate_amount(0))
# print(validate_amount(-50))
# print(validate_amount("hello"))
# print(validate_amount(""))
# print(validate_amount("NaN"))
# print(validate_amount("Infinity"))

# from validation import validate_note

# print(validate_note("Lunch with friends"))
# print(validate_note("Bought groceries"))
# print(validate_note(""))
# print(validate_note("   "))
# print(validate_note(123))
# print(validate_note(None))

# from expense import Expense
# from validation import validate_expense

# # Existing expenses
# existing_expenses = [
#     Expense(1, "2026-11-01", "Food", 15.50, "Lunch"),
#     Expense(2, "2026-11-02", "Transport", 5.00, "Taxi")
# ]

# # Test 1: All valid fields
# expense1 = Expense(3, "2026-11-08", "Shopping", 50.00, "New clothes")
# print(validate_expense(expense1, existing_expenses))

# # Test 2: Duplicate ID
# expense2 = Expense(1, "2026-11-08", "Food", 10.00, "Dinner")
# print(validate_expense(expense2, existing_expenses))

# # Test 3: Invalid date
# expense3 = Expense(4, "2026-13-40", "Food", 10.00, "Dinner")
# print(validate_expense(expense3, existing_expenses))

# # Test 4: Invalid category
# expense4 = Expense(5, "2026-11-08", "   ", 10.00, "Dinner")
# print(validate_expense(expense4, existing_expenses))

# # Test 5: Invalid amount
# expense5 = Expense(6, "2026-11-08", "Food", -10.00, "Dinner")
# print(validate_expense(expense5, existing_expenses))

# # Test 6: Invalid note
# expense6 = Expense(7, "2026-11-08", "Food", 10.00, "")
# print(validate_expense(expense6, existing_expenses))

# from validation import validate_expense_update

# # Test 1: All valid fields
# update1 = Expense(1, "2026-11-08", "Food", 25.00, "Updated lunch")
# print(validate_expense_update(update1))

# # Test 2: Invalid date
# update2 = Expense(1, "2026-15-40", "Food", 25.00, "Updated lunch")
# print(validate_expense_update(update2))

# # Test 3: Invalid category
# update3 = Expense(1, "2026-11-08", "   ", 25.00, "Updated lunch")
# print(validate_expense_update(update3))

# # Test 4: Invalid amount
# update4 = Expense(1, "2026-11-08", "Food", 0, "Updated lunch")
# print(validate_expense_update(update4))

# # Test 5: Invalid note
# update5 = Expense(1, "2026-11-08", "Food", 25.00, "")
# print(validate_expense_update(update5))