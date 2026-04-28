# Expense Tracker CLI

This project is a simple Python command-line program that saves expenses in a JSON file. The user can add an expense, list saved expenses, and see the total amount spent.

The project uses basic Python, file input/output, command-line arguments, testing with `pytest`, and GitHub Actions. The data is stored locally, so it does not need a database or internet connection.

## What It Does

- adds a new expense
- saves expenses in a JSON file
- lists saved expenses
- shows a summary of total spending

## Installation

1. Clone the repository.

```bash
git clone https://github.com/aheckart155/Expense-tracker-CLASS-PROJECT.git
cd Expense-tracker-CLASS-PROJECT
```

2. Create a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install `pytest`.

```bash
python -m pip install --upgrade pip
pip install pytest
```

## Usage

Run the program from the project folder with:

```bash
python -m expense_tracker --help
```

By default, the program saves data in `data/expenses.json`.

### Add an expense

```bash
python -m expense_tracker add 12.50 food Lunch --date 2026-04-01
```

Expected output:

```text
Added expense #1: $12.50 for food.
```

### List expenses

```bash
python -m expense_tracker list
```

Example output:

```text
1. 2026-04-01 | food | $12.50 | Lunch
```

### Show summary

```bash
python -m expense_tracker summary
```

Example output:

```text
Expense Summary
Number of expenses: 1
Total spent: $12.50
```

## Examples

Example 1:

```bash
python -m expense_tracker add 8.75 food Coffee --date 2026-04-10
python -m expense_tracker add 20.00 gas Car --date 2026-04-11
python -m expense_tracker list
```

Example 2:

```bash
python -m expense_tracker add 45.00 school Textbook --date 2026-04-15
python -m expense_tracker summary
```

Example 3:

```bash
python -m expense_tracker --data-file sample.json add 15.00 fun Movie --date 2026-04-20
python -m expense_tracker --data-file sample.json list
```

## Running Tests

```bash
python -m pytest
```

The GitHub Actions workflow in `.github/workflows/tests.yml` runs the tests automatically on every push to `main`.

## Known Limitations / Future Ideas

- expenses cannot be edited after they are saved
- categories are typed manually, so users can make spelling mistakes
- a future version could sort expenses by category or month
