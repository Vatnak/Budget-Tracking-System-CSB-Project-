from contextlib import redirect_stdout
from datetime import datetime
from decimal import Decimal
from io import StringIO
from pathlib import Path

import streamlit as st

from expense import Expense
from expense_manager import ExpenseManager
from storage import load_expenses, save_expenses
from summary import calculate_category_totals, calculate_total_expenses


DATA_FILE = Path(__file__).with_name("expenses.json")

st.set_page_config(page_title="Budget Tracker", page_icon="💸", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #f5f7fb; }
    [data-testid="stHeader"] { background: rgba(245, 247, 251, 0.85); }
    [data-testid="stSidebar"] { background: #ffffff; }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e7ebf3;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 18px rgba(31, 45, 80, 0.04);
    }
    [data-testid="stMetricLabel"] { color: #64748b; }
    .dashboard-hero {
        background: linear-gradient(120deg, #173b68 0%, #2867a7 58%, #4386bd 100%);
        border-radius: 22px;
        padding: 30px 34px;
        color: white;
        margin: 0 0 22px 0;
        box-shadow: 0 12px 30px rgba(30, 75, 125, 0.16);
    }
    .dashboard-hero .eyebrow {
        color: #c8e3ff;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        margin: 0 0 8px 0;
        text-transform: uppercase;
    }
    .dashboard-hero h1 {
        color: white;
        font-size: 2rem;
        margin: 0 0 7px 0;
    }
    .dashboard-hero p:last-child {
        color: #e2efff;
        margin: 0;
    }
    div.stButton > button[kind="primary"] {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_manager():
    try:
        saved_expenses = load_expenses(DATA_FILE)
    except (OSError, ValueError) as error:
        st.error(str(error))
        st.stop()

    manager = ExpenseManager()
    output = StringIO()
    with redirect_stdout(output):
        valid_records = all(manager.add_expense(expense) for expense in saved_expenses)
    if not valid_records:
        st.error(output.getvalue().strip() or "The saved expense data is invalid.")
        st.stop()
    return manager


def save_manager(manager):
    output = StringIO()
    with redirect_stdout(output):
        saved = save_expenses(manager.view_expense(), DATA_FILE)
    if not saved:
        st.error(output.getvalue().strip() or "Unable to save expenses.")
    return saved


def expense_rows(expenses):
    return [
        {
            "ID": expense.expense_id,
            "Date": expense.date,
            "Category": expense.category,
            "Amount (USD)": float(Decimal(str(expense.amount))),
            "Note": expense.note,
        }
        for expense in expenses
    ]


def show_expenses(expenses):
    if expenses:
        st.dataframe(expense_rows(expenses), use_container_width=True, hide_index=True)
    else:
        st.info("No expenses match these filters.")


def show_dashboard(expenses):
    st.markdown(
        """
        <div class="dashboard-hero">
            <p class="eyebrow">Personal finance overview</p>
            <h1>Your money, in focus.</h1>
            <p>Track spending, spot patterns, and stay on top of your budget.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    month_options = sorted({expense.date[:7] for expense in expenses}, reverse=True)
    control, action = st.columns([3, 1])
    selected_month = control.selectbox(
        "Reporting period",
        ["All time"] + month_options,
        format_func=lambda value: (
            value if value == "All time"
            else datetime.strptime(value, "%Y-%m").strftime("%B %Y")
        ),
    )
    action.button(
        "＋ Add an expense",
        type="primary",
        use_container_width=True,
        on_click=lambda: st.session_state.update({"page_nav": "Add expense"}),
    )

    period_expenses = expenses
    if selected_month != "All time":
        period_expenses = [
            expense for expense in expenses if expense.date.startswith(selected_month)
        ]

    total = calculate_total_expenses(period_expenses)
    categories = calculate_category_totals(period_expenses)
    first, second, third = st.columns(3)
    first.metric("Total spending", f"${total:,.2f}")
    second.metric("Expenses recorded", len(period_expenses))
    third.metric("Categories", len(categories))

    chart_column, category_column = st.columns([1.6, 1])
    chart_column.subheader("Spending overview")
    chart_type = chart_column.radio(
        "Break down spending by",
        ["Category", "Day"],
        horizontal=True,
        label_visibility="collapsed",
    )
    if categories:
        if chart_type == "Category":
            ordered_categories = sorted(categories.items(), key=lambda item: item[1], reverse=True)
            chart_data = {
                "Category": [category for category, _ in ordered_categories],
                "Amount (USD)": [float(amount) for _, amount in ordered_categories],
            }
            chart_column.bar_chart(chart_data, x="Category", y="Amount (USD)")
        else:
            daily_totals = {}
            for expense in period_expenses:
                daily_totals[expense.date] = (
                    daily_totals.get(expense.date, Decimal("0.00"))
                    + Decimal(str(expense.amount))
                )
            chart_data = {
                "Date": sorted(daily_totals),
                "Amount (USD)": [
                    float(daily_totals[day]) for day in sorted(daily_totals)
                ],
            }
            chart_column.bar_chart(chart_data, x="Date", y="Amount (USD)")
    else:
        chart_column.info("Add an expense to see your spending overview.")

    category_column.subheader("Category totals")
    if categories:
        category_rows = [
            {"Category": category, "Amount (USD)": f"${amount:,.2f}"}
            for category, amount in sorted(
                categories.items(), key=lambda item: item[1], reverse=True
            )
        ]
        category_column.dataframe(
            category_rows, use_container_width=True, hide_index=True
        )
    else:
        category_column.info("No category totals for this period.")

    st.subheader("Recent expenses")
    recent = sorted(period_expenses, key=lambda expense: expense.date, reverse=True)[:5]
    show_expenses(recent)


def show_add_expense(manager):
    st.title("Add an expense")
    with st.form("add_expense_form", clear_on_submit=True):
        date = st.date_input("Date")
        category = st.text_input("Category", placeholder="e.g. Food")
        amount = st.number_input("Amount (USD)", min_value=0.01, step=0.01, format="%.2f")
        note = st.text_input("Note", placeholder="What was this expense for?")
        submitted = st.form_submit_button("Add expense", type="primary")

    if submitted:
        expense_id = max(manager.expenses, default=0) + 1
        expense = Expense(expense_id, date.strftime("%Y-%m-%d"), category, amount, note)
        output = StringIO()
        with redirect_stdout(output):
            added = manager.add_expense(expense)
        if not added:
            st.error(output.getvalue().strip() or "Please check the expense details.")
        elif save_manager(manager):
            st.success("Expense added.")
            st.rerun()


def show_expenses_page(expenses):
    st.title("Expenses")
    categories = sorted({expense.category for expense in expenses})
    category_options = ["All categories"] + categories

    first, second = st.columns([2, 1])
    category = first.selectbox("Filter by category", category_options)
    filter_by_date = second.checkbox("Filter by date")
    selected_date = st.date_input("Date", key="expense_filter_date") if filter_by_date else None

    filtered = expenses
    if category != "All categories":
        filtered = [expense for expense in filtered if expense.category == category]
    if selected_date is not None:
        date_text = selected_date.strftime("%Y-%m-%d")
        filtered = [expense for expense in filtered if expense.date == date_text]
    show_expenses(filtered)


def show_manage_expenses(manager):
    st.title("Edit or delete an expense")
    expenses = manager.view_expense()
    if not expenses:
        st.info("There are no expenses to manage yet.")
        return

    selected = st.selectbox(
        "Choose an expense",
        expenses,
        format_func=lambda expense: (
            f"#{expense.expense_id} · {expense.date} · {expense.category} · "
            f"${Decimal(str(expense.amount)):.2f}"
        ),
    )
    date_value = datetime.strptime(selected.date, "%Y-%m-%d").date()

    st.subheader("Update details")
    with st.form(f"update_expense_{selected.expense_id}"):
        date = st.date_input("Date", value=date_value)
        category = st.text_input("Category", value=selected.category)
        amount = st.number_input(
            "Amount (USD)",
            min_value=0.01,
            value=float(selected.amount),
            step=0.01,
            format="%.2f",
        )
        note = st.text_input("Note", value=selected.note)
        submitted = st.form_submit_button("Save changes", type="primary")

    if submitted:
        output = StringIO()
        with redirect_stdout(output):
            updated = manager.update_expense(
                selected.expense_id,
                date=date.strftime("%Y-%m-%d"),
                category=category,
                amount=amount,
                note=note,
            )
        if not updated:
            st.error(output.getvalue().strip() or "Please check the expense details.")
        elif save_manager(manager):
            st.success("Expense updated.")
            st.rerun()

    st.subheader("Delete expense")
    with st.form(f"delete_expense_{selected.expense_id}"):
        confirmed = st.checkbox("I understand this expense will be permanently deleted.")
        delete_submitted = st.form_submit_button("Delete expense")
    if delete_submitted:
        if not confirmed:
            st.warning("Confirm the deletion before continuing.")
        elif manager.delete_expense(selected.expense_id) and save_manager(manager):
            st.success("Expense deleted.")
            st.rerun()


manager = load_manager()
expenses = manager.view_expense()

with st.sidebar:
    st.title("💸 Budget Tracker")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Expenses", "Add expense", "Edit / delete"],
        label_visibility="collapsed",
        key="page_nav",
    )

if page == "Dashboard":
    show_dashboard(expenses)
elif page == "Expenses":
    show_expenses_page(expenses)
elif page == "Add expense":
    show_add_expense(manager)
else:
    show_manage_expenses(manager)
