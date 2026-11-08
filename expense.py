class Expense:
    def __init__(self, expense_id, date, category, amount, note):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.amount = amount
        self.note = note

    def to_dict(self):
        return {
            "id": self.expense_id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "note": self.note
        }