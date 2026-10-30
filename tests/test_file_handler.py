import json
from pathlib import Path

import pytest

from src.file_handler import load_json_file


def test_load_valid_json(tmp_path: Path) -> None:
    """Test loading a valid JSON file."""

    path = tmp_path / "valid.json"

    expected = [
        {"prompt": "What is the sum of 2 and 3"},
        {"prompt": "Greet Shrek"},
    ]

    path.write_text(
        json.dumps(expected),
        encoding="utf-8",
    )

    result = load_json_file(str(path))

    assert result == expected


def test_load_empty_json_array(tmp_path: Path) -> None:
    """Test loading an empty JSON array"""
    path = tmp_path / "empty.json"
    path.write_text("[]", encoding="utf-8")

    assert load_json_file(str(path)) == []


def test_load_missing_file(tmp_path: Path) -> None:
    """Test handling of a missing file."""
    path = tmp_path / "missing.json"

    with pytest.raises(
        FileNotFoundError,
        match="File not found",
    ):
        load_json_file(str(path))


def test_load_invalid_json(tmp_path: Path) -> None:
    """Test handling a malformed JSON"""
    path = tmp_path / "invalid.json"
    path.write_text('{"name":}', encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Invalid JSON",
    ):
        load_json_file(str(path))
