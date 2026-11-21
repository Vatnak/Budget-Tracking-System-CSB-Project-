# Test Cases and Results

**Project:** Budget Tracking System (COSC221 Final Project)
**Test date:** 2026-11-21
**Test data:** The sample `expenses.json` (12 fictional records, IDs 1–12). Each test started from a fresh copy of this file.
**How tests were run:** CLI tests were run through `python main.py` using scripted keyboard input. The automated unit tests were run with `python -m unittest discover -s tests -v`.

## Manual Test Table (CLI)

| #  | Test case | Input / action | Expected result | Actual result | Status |
| -- | --------- | -------------- | --------------- | ------------- | ------ |
| 1  | Add a valid expense | Menu `1`; date `2026-11-21`, category `Food`, amount `5.50`, note `Lunch` | Expense is saved with the next ID (13) | "Changes saved successfully." `expenses.json` now holds 13 records; record 13 is `2026-11-21, Food, 5.5, Lunch` | Pass |
| 2  | Reject an empty required field | Menu `1`; leave the category blank | Error message; the expense is not saved | "Invalid Category: Please enter a valid category." File still holds 12 records | Pass |
| 3  | Reject a negative amount | Menu `1`; amount `-5`, then `5` | `-5` is rejected and the user is asked again | "Invalid Amount: Amount must be greater than zero". The prompt repeats, and `5` is accepted | Pass |
| 4  | Reject an invalid date format | Menu `1`; date `21-11-2026` | Error message; the expense is not saved | "Invalid Date: Please enter a valid date in the format YYYY-MM-DD." File still holds 12 records | Pass |
| 5  | Search for existing records | Menu `3`; category `Food` | All Food expenses are listed | IDs 1, 4 and 9 are listed | Pass |
| 6  | Search for a record that does not exist | Menu `3`; category `Travel` | "No expenses found." | "No expenses found." | Pass |
| 7  | Update an existing expense | Menu `4`; ID `2`, amount `3.00`, note `Tuk-tuk ride`; leave the other fields blank | Only the changed fields are updated, and the change is saved | "Changes saved successfully." | Pass |
| 8  | Update an unknown ID | Menu `4`; ID `99` | Handled without a crash | "Expense ID not found." | Pass |
| 9  | Cancel a deletion | Menu `5`; ID `12`, answer `no` | The record is kept | "Deletion cancelled." File still holds 12 records | Pass |
| 10 | Confirm a deletion | Menu `5`; ID `12`, answer `yes` | The record is removed and the change is saved | "Changes saved successfully." File holds 11 records | Pass |
| 11 | Saved records survive a restart | Add an expense, exit (`7`), restart and view all (`2`) | The new record is shown after the restart | `13 \| 2026-11-21 \| Food \| $5.50 \| Lunch` is shown | Pass |
| 12 | Start with a missing data file | Delete `expenses.json`, start the app, view all | The app starts with an empty list and does not crash | "No expenses found." The menu works normally | Pass |
| 13 | Start with a damaged JSON file | Replace the file content with `{bad json`, start the app | Clear error message; the damaged file is not overwritten | "Unable to load expenses: The JSON file is damaged. Please repair it before continuing." The file is unchanged | Pass |
| 14 | Invalid menu choice | Enter `abc`, then `9` | Error message; the menu is shown again | "Invalid choice: Please enter a number from 1 to 7." (shown twice) | Pass |
| 15 | Spending summary is accurate | Menu `6` with the 12 sample records | Total $157.30; Food $42.75, Transport $17.00, Books $18.75, Utilities $28.00, Entertainment $19.50, Health $9.80, Shopping $21.50 | The output matches the expected values exactly | Pass |

**Result: 15 of 15 manual tests passed.**

## Automated Unit Tests

| Test (`tests/test_expense_manager.py`) | What it checks | Result |
| -------------------------------------- | -------------- | ------ |
| `test_lookup_uses_id_and_duplicates_do_not_replace_records` | Records are looked up by ID; a duplicate ID does not replace an existing record | Pass |
| `test_update_validation_and_delete_by_id` | Invalid updates are rejected; deletion by ID works | Pass |
| `test_filtering_and_summaries_use_expense_objects` | Search filters and summaries work with `Expense` objects | Pass |
| `test_json_round_trip_preserves_list_format` | Saving and loading JSON keeps the same records | Pass |
| `test_failed_save_restores_dictionary_and_previous_values` | A failed save rolls the data back to its previous state | Pass |
| `test_cli_add_update_delete_integrate_with_dictionary` | CLI add, update and delete work together with the manager | Pass |

```text
Ran 6 tests in 0.012s
OK
```

## Observations

- Category search is case-sensitive. Searching for `food` does not find records saved as `Food`.
- When adding an expense in the CLI, an empty category or an invalid date is reported only after all fields have been entered. The amount is checked immediately.
