
import pytest

from src.decoder import (
    is_inside_string,
    scan_json_structure,
    classify_simple_object,
    classify_number_prefix,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        ('{"name": "Shrek"}', False),
        ('{"name": "Shrek', True),
        (r'{"message": "Hello \"Shrek\""}', False),
        ('{"name":', False),
    ],
)
def test_is_inside_string(text: str, expected: bool) -> None:
    """Test detection of open JSON strings."""
    assert is_inside_string(text) == expected


@pytest.mark.parametrize(
    "text, expected_stack, expected_inside, expected_ok",
    [
        ('{"name": "Shrek"}', [], False, True),
        ('{"name": "Shrek', ["{"], True, True),
        ('{"message": "Hello } world"}', [], False, True),
        ('{"name": {"first": "Shrek"}}', [], False, True),
        ('{"name": "Shrek"}}', [], False, False),
        ('{"items": [1, 2, 3]}', [], False, True),
        ('{"items": [1, 2, 3}', ["{", "["], False, False),
    ],
)
def test_scan_json_structure(
    text: str,
    expected_stack: list[str],
    expected_inside: bool,
    expected_ok: bool,
) -> None:
    """Test JSON delimiter scanning."""
    stack, inside, ok = scan_json_structure(text)

    assert stack == expected_stack
    assert inside == expected_inside
    assert ok == expected_ok


@pytest.mark.parametrize(
    "text, expected",
    [
        ('{"name": "Shrek"}', "COMPLETE"),
        ('{"name": "Shrek",', "VALID_PREFIX"),
        ('{"name": "Shrek",}', "INVALID"),
        ('{"name":}', "INVALID"),
        ('{"name":', "VALID_PREFIX"),
        ('{"name": "Shrek", "city": "Lyon"}', "COMPLETE"),
        ('{"name": "Shrek"}Hello', "INVALID"),
        ('{}', "COMPLETE"),
    ],
)
def test_classify_simple_object(text: str, expected: str) -> None:
    """Test prefix classification for simple JSON objects."""
    assert classify_simple_object(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("42", "COMPLETE"),
        ("-42", "COMPLETE"),
        ("0", "COMPLETE"),
        ("-0", "COMPLETE"),
        ("3.14", "COMPLETE"),
        ("-0.5", "COMPLETE"),
        ("0.001", "COMPLETE"),
        ("1e3", "COMPLETE"),
        ("2E-4", "COMPLETE"),
        ("3.14e+2", "COMPLETE"),
        ("0e3", "COMPLETE"),
        ("1e-", "VALID_PREFIX"),
        ("1e", "VALID_PREFIX"),
        ("3.", "VALID_PREFIX"),
        ("-", "VALID_PREFIX"),
        ("01", "INVALID"),
        ("--4", "INVALID"),
        ("+4", "INVALID"),
        ("1.2.3", "INVALID"),
        (".5", "INVALID"),
        ("1e--3", "INVALID"),
        ("1.2e3.4", "INVALID"),
    ],
)
def test_classify_number_prefix(text: str, expected: str) -> None:
    """Test JSON number prefix classification."""
    assert classify_number_prefix(text) == expected
