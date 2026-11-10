import json
from expense import Expense


def save_expenses(expenses, filename="expenses.json"):
    records = []

    for expense in expenses:
        records.append(expense.to_dict())

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
        return True
    except OSError:
        print("Unable to save expenses: Please check the file location and permissions.")
        return False


def load_expenses(filename="expenses.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("Unable to load expenses: The JSON file is damaged. Please repair it before continuing.") from error

    if not isinstance(records, list):
        raise ValueError("Unable to load expenses: The JSON file must contain a list of expenses.")

    expenses = []

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Unable to load expenses: Each expense must be a JSON object.")

        try:
            expense = Expense(
                record["id"],
                record["date"],
                record["category"],
                record["amount"],
                record["note"]
            )
        except KeyError as error:
            raise ValueError("Unable to load expenses: An expense is missing a required field.") from error

        expenses.append(expense)

    return expenses
