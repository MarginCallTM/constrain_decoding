def select_token(
    logits: list[float],
    allowed_tokens: list[int]
) -> int:
    if not allowed_tokens:
        raise ValueError("No allowed tokens available")
    best_token = allowed_tokens[0]
    best_score = logits[best_token]

    for token_id in allowed_tokens:
        score = logits[token_id]

        if score > best_score:
            best_score = score
            best_token = token_id

    return best_token


if __name__ == "__main__":
    logits = [2.5, 8.7, 4.2, 9.1]
    allowed_tokens = [0, 1, 2]

    result = select_token(logits, allowed_tokens)
    print(result)
