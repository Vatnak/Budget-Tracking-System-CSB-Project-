from decimal import Decimal


def calculate_total_expenses(expenses):
    total = Decimal("0.00")

    for expense in expenses:
        total += Decimal(str(expense.amount))

    return total


def calculate_category_totals(expenses):
    category_totals = {}

    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = Decimal("0.00")

        category_totals[expense.category] += Decimal(str(expense.amount))

    return category_totals
