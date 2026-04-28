from datetime import date, datetime
import json
from pathlib import Path
from typing import Optional


class TrackerError(ValueError):
    pass


def load_expenses(path: Path) -> list[dict]:
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise TrackerError("Data file is not valid JSON.") from error

    if not isinstance(data, list):
        raise TrackerError("Data file must contain a list.")

    return data


def save_expenses(path: Path, expenses: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(expenses, indent=2) + "\n", encoding="utf-8")


def parse_amount(value: str) -> float:
    try:
        amount = float(value)
    except ValueError as error:
        raise TrackerError("Amount must be a number.") from error

    if amount <= 0:
        raise TrackerError("Amount must be greater than 0.")

    return round(amount, 2)


def parse_date(value: Optional[str]) -> str:
    if value is None:
        return date.today().isoformat()

    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise TrackerError("Date must be in YYYY-MM-DD format.") from error

    return value


def next_id(expenses: list[dict]) -> int:
    if not expenses:
        return 1
    return max(expense["id"] for expense in expenses) + 1


def add_expense(
    path: Path,
    amount: str,
    category: str,
    description: str,
    expense_date: Optional[str] = None,
) -> dict:
    category = category.strip()
    description = description.strip()

    if not category:
        raise TrackerError("Category cannot be empty.")

    expenses = load_expenses(path)
    expense = {
        "id": next_id(expenses),
        "amount": parse_amount(amount),
        "category": category,
        "description": description,
        "date": parse_date(expense_date),
    }
    expenses.append(expense)
    save_expenses(path, expenses)
    return expense


def get_summary(expenses: list[dict]) -> dict:
    total = round(sum(expense["amount"] for expense in expenses), 2)
    return {"count": len(expenses), "total": total}


def format_money(amount: float) -> str:
    return f"${amount:.2f}"
