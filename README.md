# Budget Tracking System

**COSC221 – Final Project**  
**American University of Phnom Penh (AUPP)**  
**Programming Language:** Python  
**Application Type:** Command-Line Interface (CLI)  
**Data Storage:** JSON  
**Team:** [Team Number]

## 1. Project Overview

The Budget Tracking System is a Python command-line application designed to help users record, manage, and monitor their daily expenses.

The application allows users to add, view, search, update, and delete expense records. It also provides spending summaries to help users understand their financial activities.

The project focuses on implementing fundamental Python programming concepts, including Object-Oriented Programming (OOP), data structures, file handling, input validation, and error handling.

## 2. Project Objectives

- Develop a functional Python application for managing personal expenses.
- Implement Create, Read, Update, and Delete (CRUD) operations.
- Store expense information permanently using JSON.
- Apply Object-Oriented Programming principles.
- Validate user inputs and handle errors appropriately.
- Generate spending summaries based on recorded expenses.
- Provide a simple and user-friendly command-line interface.

## 3. Features

### Core Features

| Feature | Description |
|---|---|
| Add Expense | Create an expense record with a unique ID. |
| View Expenses | Display all recorded expenses. |
| Search Expenses | Search or filter expenses by category or date. |
| Update Expense | Modify an existing expense using its ID. |
| Delete Expense | Delete an expense after user confirmation. |
| Save and Load | Save expense records to JSON and load them when restarting. |
| Spending Summary | Display total expenses and spending totals by category. |

**Development status:** Planned. Update this section as features are completed and tested.

## 4. Expense Record Structure

Each expense contains the following information:

| Field | Description | Example |
|---|---|---|
| ID | Unique expense identifier | 1 |
| Date | Date of expense (YYYY-MM-DD) | 2026-11-07 |
| Category | Expense category | Food |
| Amount | Amount spent in USD | 5.50 |
| Note | Short description | Lunch |

### Example JSON Record

```json
{
  "id": 1,
  "date": "2026-11-07",
  "category": "Food",
  "amount": 5.50,
  "note": "Lunch"
}
```

## 5. Technologies Used

- **Python 3:** Main programming language.
- **JSON:** Persistent storage for expense records.
- **Python OOP:** Used to organize expense records and management operations.
- **List/Dictionary:** Used to store and access records in memory.
- **Git/GitHub:** Recommended for team collaboration and version control.

The application is designed to use Python's standard library without requiring external packages.

## 6. Project Structure

The planned project structure is:

```text
Budget-Tracking-System/
│
├── main.py
├── expense.py
├── expense_manager.py
├── storage.py
├── validation.py
├── summary.py
│
├── expenses.json
├── test_cases.md
└── README.md
```

### File Descriptions

| File | Responsibility |
|---|---|
| `main.py` | Main application and CLI menu |
| `expense.py` | Expense class and record attributes |
| `expense_manager.py` | Add, view, search, update, and delete operations |
| `storage.py` | JSON file saving and loading |
| `validation.py` | Validation of dates, amounts, and other inputs |
| `summary.py` | Spending calculations and category summaries |
| `expenses.json` | Stored expense records |
| `test_cases.md` | Test cases and results |
| `README.md` | Project documentation |

## 7. Installation and Setup

### Prerequisites

- Python 3 installed.
- A terminal or command prompt.
- A code editor such as Visual Studio Code (optional).

### Running the Application

1. Download or clone the project repository.
2. Open the project folder in a terminal.
3. Run the following command:

```bash
python main.py
```

On systems where `python3` is required:

```bash
python3 main.py
```

4. Follow the instructions displayed in the command-line menu.

**Note:** These instructions assume the completed application uses `main.py` as its entry point.

## 8. Application Menu

The planned menu is:

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

Testing will verify that the required application features function correctly.

The team will document at least eight test checks, including:

1. Adding a valid expense.
2. Rejecting an empty required field.
3. Rejecting a negative expense amount.
4. Searching for existing and nonexistent records.
5. Updating an existing expense.
6. Cancelling and confirming deletion.
7. Restarting the application and verifying saved records.
8. Starting the application with a missing data file.

Additional checks will verify the accuracy of spending summary calculations.

Test results will be documented in `test_cases.md`, including the input/action, expected result, actual result, and pass/fail status.

## 12. Team Members and Contributions

| Member | Name | Responsibility |
|---|---|---|
| Member 1 | [Full Name] | Main application, CLI menu, module integration |
| Member 2 | [Full Name] | Expense class and CRUD operations |
| Member 3 | [Full Name] | JSON storage, file handling, input validation |
| Member 4 | [Full Name] | Spending summaries, testing, documentation |

All members will participate in final integration, testing, and project demonstration.

## 13. Development Timeline

| Week | Milestone | Deliverable |
|---|---|---|
| Week 1 | Project Proposal | Topic, team roles, record fields, menu design |
| Week 2 | First Working Version | Add, view, and search expenses |
| Week 3 | Core Implementation | Update, delete, persistence, summaries, validation |
| Week 4 | Finalization | Testing, documentation, final application, demonstration |

## 14. Known Limitations

The following are planned scope limitations, not confirmed software defects:

- The application uses a command-line interface rather than a graphical interface.
- Expense records are stored locally in a JSON file.
- The application does not support multiple user accounts.
- No cloud synchronization is included.
- No external database is required.
- Advanced financial analysis and automatic bank integration are outside the project scope.

Additional known bugs or limitations should be documented here after testing.

## 15. Final Submission

The final project submission will include:

- Complete Python source code.
- A sample JSON file containing at least 10 fictional expense records.
- This README file with finalized team information.
- A testing table showing expected and actual results.
- A brief contribution statement for each team member.

All files will be packaged into one ZIP file:

`COSC221_TeamName_FinalProject.zip`

Replace `TeamName` with the registered team number.

The team will present a **5–7 minute live demonstration**, followed by individual questions from the instructor.

## 16. Conclusion

The Budget Tracking System aims to provide a simple and reliable way to manage personal expenses while demonstrating practical Python programming skills.

By implementing Object-Oriented Programming, CRUD operations, JSON file storage, error handling, and spending summaries, the project fulfills the technical learning objectives of COSC221.

---

**Course:** COSC221  
**Institution:** American University of Phnom Penh  
**Project Type:** Final Group Project  
**Status:** In Development