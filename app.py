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
PAGE_ICON = Path(__file__).parent.parent / "10986471.png"

st.set_page_config(page_title="Budget Tracker",
                   page_icon=str(PAGE_ICON), layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #f5f7fb; }
    [data-testid="stHeader"] { background: rgba(245, 247, 251, 0.85); }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"],
    [data-testid="stSidebar"] [data-testid="stRadio"] > div,
    [data-testid="stSidebar"] [role="radiogroup"] {
        width: 100%;
    }
    [data-testid="stSidebar"] [role="radiogroup"] {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 8px;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        width: 100%;
        box-sizing: border-box;
        min-height: 44px;
        display: flex;
        align-items: center;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 0;
        cursor: pointer;
        transition: background 0.15s, border-color 0.15s;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #eef2ff;
        border-color: #c7d2fe;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: #2563eb;
        border-color: #2563eb;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
        color: #ffffff;
        font-weight: 600;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label > div:not(:has([data-testid="stMarkdownContainer"])) {
        display: none !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label > div {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    [data-testid="stMetric"],
    [class*="st-key-box-"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: none;
    }
    [data-testid="stMetric"] {
        padding: 16px 18px;
    }
    [data-testid="stMetricLabel"] p {
        color: #6b7280;
        font-size: 0.85rem;
    }
    .page-header h1 {
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0;
        padding: 0;
    }
    .page-header p {
        color: #6b7280;
        margin: 4px 0 16px 0;
    }
    .box-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0 0 8px 0;
    }
    div.stButton > button {
        border-radius: 6px;
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
        valid_records = all(manager.add_expense(expense)
                            for expense in saved_expenses)
    if not valid_records:
        st.error(output.getvalue().strip()
                 or "The saved expense data is invalid.")
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
        st.dataframe(expense_rows(expenses),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No expenses match these filters.")


def show_pie_chart(container, chart_data, label_field):
    rows = [
        {label_field: label, "Amount (USD)": amount}
        for label, amount in zip(chart_data[label_field], chart_data["Amount (USD)"])
    ]
    container.vega_lite_chart(
        {
            "data": {"values": rows},
            "mark": {"type": "arc", "innerRadius": 60, "stroke": "#ffffff"},
            "encoding": {
                "theta": {"field": "Amount (USD)", "type": "quantitative", "stack": True},
                "color": {
                    "field": label_field,
                    "type": "nominal",
                    "sort": None,
                    "legend": {"title": label_field, "orient": "right"},
                },
                "order": {"field": "Amount (USD)", "type": "quantitative", "sort": "descending"},
                "tooltip": [
                    {"field": label_field, "type": "nominal"},
                    {"field": "Amount (USD)", "type": "quantitative", "format": "$,.2f"},
                ],
            },
            "height": 320,
        },
        use_container_width=True,
    )


def show_dashboard(expenses):
    st.markdown(
        '<div class="page-header"><h1>Dashboard</h1>'
        "<p>Spending summary for the selected period.</p></div>",
        unsafe_allow_html=True,
    )

    month_options = sorted({expense.date[:7]
                           for expense in expenses}, reverse=True)
    control, _, action = st.columns([2, 2, 1], vertical_alignment="bottom")
    selected_month = control.selectbox(
        "Period",
        ["All time"] + month_options,
        format_func=lambda value: (
            value if value == "All time"
            else datetime.strptime(value, "%Y-%m").strftime("%B %Y")
        ),
    )
    action.button(
        "Add expense",
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
    first.metric("Total spent", f"${total:,.2f}")
    second.metric("Expenses", len(period_expenses))
    third.metric("Categories", len(categories))

    chart_area, category_area = st.columns([1.6, 1])
    chart_column = chart_area.container(border=True, key="box-chart")
    category_column = category_area.container(border=True, key="box-categories")

    title, toggle = chart_column.columns([1, 1], vertical_alignment="center")
    title.markdown('<p class="box-title">Spending</p>', unsafe_allow_html=True)
    chart_type = toggle.segmented_control(
        "Break down spending by",
        ["Category", "Day"],
        default="Category",
        label_visibility="collapsed",
    ) or "Category"
    if categories:
        if chart_type == "Category":
            ordered_categories = sorted(
                categories.items(), key=lambda item: item[1], reverse=True)
            chart_data = {
                "Category": [category for category, _ in ordered_categories],
                "Amount (USD)": [float(amount) for _, amount in ordered_categories],
            }
            show_pie_chart(chart_column, chart_data, "Category")
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
            show_pie_chart(chart_column, chart_data, "Date")
    else:
        chart_column.info("Add an expense to see your spending overview.")

    category_column.markdown(
        '<p class="box-title">By category</p>', unsafe_allow_html=True)
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

    recent_box = st.container(border=True, key="box-recent")
    recent_box.markdown(
        '<p class="box-title">Recent expenses</p>', unsafe_allow_html=True)
    recent = sorted(period_expenses,
                    key=lambda expense: expense.date, reverse=True)[:5]
    with recent_box:
        show_expenses(recent)


def show_add_expense(manager):
    st.title("Add an expense")
    with st.form("add_expense_form", clear_on_submit=True):
        date = st.date_input("Date")
        category = st.text_input("Category", placeholder="e.g. Food")
        amount = st.number_input(
            "Amount (USD)", min_value=0.01, step=0.01, format="%.2f")
        note = st.text_input("Note", placeholder="What was this expense for?")
        submitted = st.form_submit_button("Add expense", type="primary")

    if submitted:
        expense_id = max(manager.expenses, default=0) + 1
        expense = Expense(expense_id, date.strftime(
            "%Y-%m-%d"), category, amount, note)
        output = StringIO()
        with redirect_stdout(output):
            added = manager.add_expense(expense)
        if not added:
            st.error(output.getvalue().strip()
                     or "Please check the expense details.")
        elif save_manager(manager):
            st.session_state["success_message"] = "Expense added successfully."
            st.rerun()


def show_expenses_page(expenses):
    st.title("Expenses")
    categories = sorted({expense.category for expense in expenses})
    category_options = ["All categories"] + categories

    first, second = st.columns([2, 1])
    category = first.selectbox("Filter by category", category_options)
    filter_by_date = second.checkbox("Filter by date")
    selected_date = st.date_input(
        "Date", key="expense_filter_date") if filter_by_date else None

    filtered = expenses
    if category != "All categories":
        filtered = [
            expense for expense in filtered if expense.category == category]
    if selected_date is not None:
        date_text = selected_date.strftime("%Y-%m-%d")
        filtered = [
            expense for expense in filtered if expense.date == date_text]
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
            st.error(output.getvalue().strip()
                     or "Please check the expense details.")
        elif save_manager(manager):
            st.session_state["success_message"] = "Expense updated successfully."
            st.rerun()

    st.subheader("Delete expense")
    with st.form(f"delete_expense_{selected.expense_id}"):
        confirmed = st.checkbox(
            "I understand this expense will be permanently deleted.")
        delete_submitted = st.form_submit_button("Delete expense")
    if delete_submitted:
        if not confirmed:
            st.warning("Confirm the deletion before continuing.")
        elif manager.delete_expense(selected.expense_id) and save_manager(manager):
            st.session_state["success_message"] = "Expense deleted successfully."
            st.rerun()


manager = load_manager()
expenses = manager.view_expense()

with st.sidebar:
    st.markdown("### Budget Tracker")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Expenses", "Add expense", "Edit / delete"],
        label_visibility="collapsed",
        key="page_nav",
    )

success_message = st.session_state.pop("success_message", None)
if success_message:
    st.success(success_message)

if page == "Dashboard":
    show_dashboard(expenses)
elif page == "Expenses":
    show_expenses_page(expenses)
elif page == "Add expense":
    show_add_expense(manager)
else:
    show_manage_expenses(manager)
