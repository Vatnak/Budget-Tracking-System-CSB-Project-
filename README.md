# Budget Tracking System

**COSC221 – Final Project**  
**American University of Phnom Penh (AUPP)**  
**Programming Language:** Python  
**Application Type:** Streamlit web GUI and command-line interface (CLI)  
**Data Storage:** JSON  
**Team:** Team 6

## 1. Project Overview

The Budget Tracking System is a Python application designed to help users record, manage, and monitor their daily expenses. It includes a Streamlit graphical interface as well as a command-line interface.

The application allows users to add, view, search, update, and delete expense records. It also provides spending summaries to help users understand their financial activities.

The project focuses on implementing fundamental Python programming concepts, including Object-Oriented Programming (OOP), data structures, file handling, input validation, and error handling.

## 2. Project Objectives

- Develop a functional Python application for managing personal expenses.
- Implement Create, Read, Update, and Delete (CRUD) operations.
- Store expense information permanently using JSON.
- Apply Object-Oriented Programming principles.
- Validate user inputs and handle errors appropriately.
- Generate spending summaries based on recorded expenses.
- Provide a simple and user-friendly graphical interface, with the CLI available as an alternative.

## 3. Features

### Core Features

| Feature          | Description                                                 |
| ---------------- | ----------------------------------------------------------- |
| Add Expense      | Create an expense record with a unique ID.                  |
| View Expenses    | Display all recorded expenses.                              |
| Search Expenses  | Search or filter expenses by category or date.              |
| Update Expense   | Modify an existing expense using its ID.                    |
| Delete Expense   | Delete an expense after user confirmation.                  |
| Save and Load    | Save expense records to JSON and load them when restarting. |
| Spending Summary | Display total expenses and spending totals by category.     |

The Streamlit interface provides these features using the existing JSON storage and validation modules.

## 4. Expense Record Structure

Each expense contains the following information:

| Field    | Description                  | Example    |
| -------- | ---------------------------- | ---------- |
| ID       | Unique expense identifier    | 1          |
| Date     | Date of expense (YYYY-MM-DD) | 2026-11-07 |
| Category | Expense category             | Food       |
| Amount   | Amount spent in USD          | 5.50       |
| Note     | Short description            | Lunch      |

### Example JSON Record

```json
{
  "id": 1,
  "date": "2026-11-07",
  "category": "Food",
  "amount": 5.5,
  "note": "Lunch"
}
```

## 5. Technologies Used

- **Python 3:** Main programming language.
- **JSON:** Persistent storage for expense records.
- **Streamlit:** Browser-based graphical interface.
- **Python OOP:** Used to organize expense records and management operations.
- **List/Dictionary:** Used to store and access records in memory.
- **Git/GitHub:** Recommended for team collaboration and version control.

The core expense-management modules use Python's standard library. The graphical interface uses Streamlit.

## 6. Project Structure

The project structure is:

```text
Budget-Tracking-System/
│
├── .streamlit/
│   └── config.toml
├── tests/
│   ├── test_expense_manager.py
│   └── test_validation.py
├── app.py
├── main.py
├── expense.py
├── expense_manager.py
├── storage.py
├── validation.py
├── summary.py
│
├── expenses.json
├── requirements.txt
├── test_cases.md
└── README.md
```

### File Descriptions

| File                 | Responsibility                                   |
| -------------------- | ------------------------------------------------ |
| `app.py`             | Streamlit graphical application                  |
| `main.py`            | Command-line application                         |
| `expense.py`         | Expense class and record attributes              |
| `expense_manager.py` | Add, view, search, update, and delete operations |
| `storage.py`         | JSON file saving and loading                     |
| `validation.py`      | Validation of dates, amounts, and other inputs   |
| `summary.py`         | Spending calculations and category summaries     |
| `expenses.json`      | Stored expense records                           |
| `requirements.txt`   | Python dependency for the Streamlit GUI          |
| `.streamlit/config.toml` | Streamlit light theme settings               |
| `tests/`             | Automated unit tests                             |
| `test_cases.md`      | Test cases and results                           |
| `README.md`          | Project documentation                            |

## 7. Installation and Setup

### Prerequisites

- Python 3 installed.
- A terminal or command prompt.
- A code editor such as Visual Studio Code (optional).

### Running the Streamlit GUI

1. Download or clone the project repository and open its folder in a terminal.
2. Install the GUI dependency:

```bash
python -m pip install -r requirements.txt
```

3. Start the graphical application:

```bash
python -m streamlit run app.py
```

Streamlit opens the Budget Tracker in your browser. Use the sidebar to navigate between the dashboard, expense list, add form, and edit/delete page. The GUI reads and saves data in `expenses.json`.

### Running the command-line version

To run the original command-line interface instead:

```bash
python main.py
```

## 8. Application Menu

The command-line menu is:

```text
================================
      BUDGET TRACKING SYSTEM
================================

1. Add Expense
2. View All Expenses
3. Search / Filter Expenses
4. Update Expense
5. Delete Expense
6. View Spending Summary
7. Exit

================================
Enter your choice:
```

Users select a menu option by entering the corresponding number.

## 9. Data Storage

The application uses a JSON file (`expenses.json`) for persistent data storage.

Expense records are stored in a Python collection during program execution and saved to JSON after successful changes.

When the application restarts, previously saved records are loaded automatically.

The application is designed to handle:

- Missing data files without crashing.
- Invalid or corrupted JSON data with clear error messages.
- Preservation of damaged files to prevent accidental data loss.
- Saving successful updates and deletions.

## 10. Input Validation and Error Handling

The application will validate user inputs to ensure data accuracy.

Validation rules include:

- Expense IDs must be unique.
- Dates must follow the `YYYY-MM-DD` format.
- Expense amounts must be valid positive numbers.
- Required fields cannot be empty.
- Unknown expense IDs must be handled gracefully.
- Deleting an expense requires confirmation.
- Invalid menu selections must not crash the application.

## 11. Testing

Testing verified that the required application features work correctly. The team documented 15 manual test checks and 6 automated unit tests. All tests passed.

The manual checks include:

1. Adding a valid expense.
2. Rejecting an empty required field.
3. Rejecting a negative expense amount.
4. Searching for existing and nonexistent records.
5. Updating an existing expense.
6. Cancelling and confirming deletion.
7. Restarting the application and verifying saved records.
8. Starting the application with a missing data file.

Additional checks verified invalid dates, unknown IDs, damaged JSON files, invalid menu choices, and the accuracy of the spending summary.

The full testing table is in [`test_cases.md`](test_cases.md). It lists the input/action, expected result, actual result, and pass/fail status for each test.

To run the automated unit tests:

```bash
python -m unittest discover -s tests -v
```

## 12. Team Members and Contributions

| Member   | Name             | Role                         | Responsibility                                                      |
| -------- | ---------------- | ---------------------------- | ------------------------------------------------------------------- |
| Member 1 | Taing Tumvatanak | Orchestrator                 | Whole pipeline: project setup, CRUD operations, CLI, JSON storage, integration |
| Member 2 | Mao Sereyvatanak | Validation                   | Input validation functions and validation tests                     |
| Member 3 | Houn Viriyaputta | User interface               | Streamlit graphical interface                                       |
| Member 4 | Art Oudom        | Testing and refinement       | Testing, test documentation, UI refinement, final README            |

### Contribution Statements

**Taing Tumvatanak (Orchestrator):** Handled the whole project pipeline. Created the repository and the file structure, and planned how the modules connect. Built the `Expense` class and the add, view, search, update, and delete operations in `expense_manager.py`. Wrote the command-line menu in `main.py`, the JSON save and load functions in `storage.py`, and the spending summaries. Integrated the validation and GUI work into the main branch, and changed the expense storage to a dictionary keyed by ID for faster lookups.

**Mao Sereyvatanak (Validation):** Wrote the input validation functions in `validation.py` for expense IDs, dates, categories, amounts, and notes. Wrote the validation test cases, and updated `.gitignore` to exclude Python cache files.

**Houn Viriyaputta (User interface):** Built the Streamlit graphical interface in `app.py`, including the dashboard, the expense list, the add form, and the edit/delete page. Connected the GUI to the existing storage and validation modules.

**Art Oudom (Testing and refinement):** Tested all application features and documented 15 manual tests and 6 unit tests in `test_cases.md`. Prepared the sample data file. Refined the GUI with a light theme, boxed sidebar navigation, and a pie chart for spending, and finalized the README.

All members participated in final integration, testing, and the project demonstration.

## 13. Development Timeline

| Week   | Milestone             | Deliverable                                              |
| ------ | --------------------- | -------------------------------------------------------- |
| Week 1 | Project Proposal      | Topic, team roles, record fields, menu design            |
| Week 2 | First Working Version | Add, view, and search expenses                           |
| Week 3 | Core Implementation   | Update, delete, persistence, summaries, validation       |
| Week 4 | Finalization          | Testing, documentation, final application, demonstration |

## 14. Known Limitations

The following are planned scope limitations, not confirmed software defects:

- The application has a local GUI and CLI, but no multi-user accounts.
- Expense records are stored locally in a JSON file.
- The application does not support multiple user accounts.
- No cloud synchronization is included.
- No external database is required.
- Advanced financial analysis and automatic bank integration are outside the project scope.

Limitations found during testing:

- Category search is case-sensitive. Searching for `food` does not find records saved as `Food`.
- In the CLI, an empty category or an invalid date is reported only after all fields have been entered.

## 15. Final Submission

The final project submission includes:

| Requirement | Location | Status |
| ----------- | -------- | ------ |
| Complete Python source code | `app.py`, `main.py`, `expense.py`, `expense_manager.py`, `storage.py`, `validation.py`, `summary.py`, `tests/` | Complete |
| Sample JSON file with at least 10 fictional expense records | `expenses.json` (12 records) | Complete |
| README with finalized team information | This file, section 12 | Complete |
| Testing table with expected and actual results | `test_cases.md` (15 manual tests, 6 unit tests) | Complete |
| Brief contribution statement for each team member | Section 12, "Contribution Statements" | Complete |

All files will be packaged into one ZIP file:

`COSC221_Team6_FinalProject.zip`

The team will present a **5–7 minute live demonstration**, followed by individual questions from the instructor.

## 16. Conclusion

The Budget Tracking System aims to provide a simple and reliable way to manage personal expenses while demonstrating practical Python programming skills.

By implementing Object-Oriented Programming, CRUD operations, JSON file storage, error handling, and spending summaries, the project fulfills the technical learning objectives of COSC221.

---

**Course:** COSC221  
**Institution:** American University of Phnom Penh  
**Project Type:** Final Group Project  
**Status:** Completed
