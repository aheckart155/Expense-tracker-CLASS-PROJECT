import argparse
from pathlib import Path
import sys
from typing import Optional

from .tracker import TrackerError, add_expense, format_money, get_summary, load_expenses

DEFAULT_DATA_FILE = Path("data/expenses.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    parser.add_argument(
        "--data-file",
        default=str(DEFAULT_DATA_FILE),
        help="Path to the JSON file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("amount")
    add_parser.add_argument("category")
    add_parser.add_argument("description")
    add_parser.add_argument("--date", dest="expense_date")

    subparsers.add_parser("list", help="Show all expenses")
    subparsers.add_parser("summary", help="Show total spending")

    return parser


def list_output(data_file: Path) -> str:
    expenses = load_expenses(data_file)

    if not expenses:
        return "No expenses found."

    lines = []
    for expense in expenses:
        line = (
            f"{expense['id']}. {expense['date']} | "
            f"{expense['category']} | "
            f"{format_money(expense['amount'])} | "
            f"{expense['description']}"
        )
        lines.append(line)

    return "\n".join(lines)


def summary_output(data_file: Path) -> str:
    expenses = load_expenses(data_file)
    summary = get_summary(expenses)
    return "\n".join(
        [
            "Expense Summary",
            f"Number of expenses: {summary['count']}",
            f"Total spent: {format_money(summary['total'])}",
        ]
    )


def run_command(args: argparse.Namespace) -> str:
    data_file = Path(args.data_file)

    if args.command == "add":
        expense = add_expense(
            data_file,
            amount=args.amount,
            category=args.category,
            description=args.description,
            expense_date=args.expense_date,
        )
        return (
            f"Added expense #{expense['id']}: "
            f"{format_money(expense['amount'])} "
            f"for {expense['category']}."
        )

    if args.command == "list":
        return list_output(data_file)

    if args.command == "summary":
        return summary_output(data_file)

    raise TrackerError("Unknown command.")


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        output = run_command(args)
    except (OSError, TrackerError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(output)
    return 0
