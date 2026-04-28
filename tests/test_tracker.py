import pytest

from expense_tracker.cli import main
from expense_tracker.tracker import TrackerError, add_expense, get_summary, load_expenses


def test_add_expense_creates_file_and_saves_data(tmp_path):
    data_file = tmp_path / "expenses.json"

    expense = add_expense(data_file, "12.50", "food", "Lunch", "2026-04-01")
    saved = load_expenses(data_file)

    assert data_file.exists()
    assert expense["id"] == 1
    assert saved[0]["category"] == "food"
    assert saved[0]["amount"] == 12.5


def test_add_expense_uses_next_id(tmp_path):
    data_file = tmp_path / "expenses.json"

    first = add_expense(data_file, "10", "food", "Lunch", "2026-04-01")
    second = add_expense(data_file, "20", "gas", "Car", "2026-04-02")

    assert first["id"] == 1
    assert second["id"] == 2


def test_add_expense_rejects_bad_amount(tmp_path):
    data_file = tmp_path / "expenses.json"

    with pytest.raises(TrackerError, match="greater than 0"):
        add_expense(data_file, "0", "food", "Lunch", "2026-04-01")


def test_add_expense_rejects_bad_date(tmp_path):
    data_file = tmp_path / "expenses.json"

    with pytest.raises(TrackerError, match="YYYY-MM-DD"):
        add_expense(data_file, "12.50", "food", "Lunch", "04-01-2026")


def test_summary_adds_all_expenses(tmp_path):
    data_file = tmp_path / "expenses.json"
    add_expense(data_file, "12.50", "food", "Lunch", "2026-04-01")
    add_expense(data_file, "20.00", "gas", "Car", "2026-04-02")

    summary = get_summary(load_expenses(data_file))

    assert summary["count"] == 2
    assert summary["total"] == 32.5


def test_cli_list_prints_saved_expenses(tmp_path, capsys):
    data_file = tmp_path / "expenses.json"
    add_expense(data_file, "12.50", "food", "Lunch", "2026-04-01")

    exit_code = main(["--data-file", str(data_file), "list"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "2026-04-01" in captured.out
    assert "food" in captured.out
    assert "$12.50" in captured.out


def test_cli_summary_prints_total(tmp_path, capsys):
    data_file = tmp_path / "expenses.json"
    add_expense(data_file, "12.50", "food", "Lunch", "2026-04-01")
    add_expense(data_file, "7.50", "school", "Notebook", "2026-04-02")

    exit_code = main(["--data-file", str(data_file), "summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Number of expenses: 2" in captured.out
    assert "Total spent: $20.00" in captured.out
