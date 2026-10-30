import pytest

from src.select_token import select_token


@pytest.mark.parametrize(
    "logits, allowed_tokens, expected",
    [
        ([0.5, 9.0, 3.0], [0, 1, 2], 1),
        ([0.5, 9.0, 3.0], [0, 2], 2),
        ([-5.0, -1.0, -3.0], [0, 1, 2], 1),
        ([1.0, 4.0, 2.0], [0], 0),
        ([1.0, 4.0, 4.0], [2, 1], 2),
    ],
)
def test_select_token(
    logits: list[float],
    allowed_tokens: list[int],
    expected: int,
) -> None:
    """Select the highest-scoring allowed token."""
    assert select_token(logits, allowed_tokens) == expected


def test_select_token_with_empty_candidates() -> None:
    """Reject an empty list of allowed tokens"""
    with pytest.raises(
        ValueError,
        match="No allowed tokens available",
    ):
        select_token([0.5, 3.0], [])
