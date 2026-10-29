import json


def is_inside_string(text: str) -> bool:
    """Check whether a JSON text prefix end inside a string"""

    in_string = False
    escaped = False

    for char in text:
        if escaped:
            escaped = False
            continue

        if char == "\\" and in_string:
            escaped = True
            continue

        if char == '"':
            in_string = not in_string

    return in_string


def scan_json_structure(text: str) -> tuple[list[str], bool, bool]:
    """Scan JSON delimiters without validating the complete JSON grammar"""

    stack: list[str] = []
    in_string = False
    escaped = False

    for char in text:
        # We are in a string
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        # Open a new chain
        if char == '"':
            in_string = True

        # Open a object or table
        elif char in "{[":
            stack.append(char)

        # Close object or table
        elif char in "}]":
            if not stack:
                return stack, in_string, False

            expected = "{" if char == "}" else "["

            if stack[-1] != expected:
                return stack, in_string, False

            stack.pop()

    return stack, in_string, True


def classify_simple_object(text: str) -> str:
    """Classify a JSON object prefix with string keys and values."""

    state = "EXPECT_OPEN"
    escaped = False

    for char in text:

        # Inside a key or a string value
        if state in ("IN_KEY", "IN_VALUE"):
            if escaped:
                escaped = False

            elif char == "\\":
                escaped = True

            elif char == '"':
                if state == "IN_KEY":
                    state = "EXPECT_COLON"
                else:
                    state = "EXPECT_COMMA_OR_END"

            continue

        # Ignore JSON whitespace outside strings
        if char in " \t\n\r":
            continue

        # Expect the opening brace
        if state == "EXPECT_OPEN":
            if char != "{":
                return "INVALID"

            state = "EXPECT_KEY_OR_END"

        # After opening an object: key or closing brace
        elif state == "EXPECT_KEY_OR_END":
            if char == '"':
                state = "IN_KEY"
            elif char == "}":
                state = "COMPLETE"
            else:
                return "INVALID"

        # After a comma: a new key is mandatory
        elif state == "EXPECT_KEY":
            if char == '"':
                state = "IN_KEY"
            else:
                return "INVALID"

        # After a key: expect a colon
        elif state == "EXPECT_COLON":
            if char == ":":
                state = "EXPECT_VALUE"
            else:
                return "INVALID"

        # After a colon: expect a string value
        elif state == "EXPECT_VALUE":
            if char == '"':
                state = "IN_VALUE"
            else:
                return "INVALID"

        # After a value: comma or closing brace
        elif state == "EXPECT_COMMA_OR_END":
            if char == ",":
                state = "EXPECT_KEY"
            elif char == "}":
                state = "COMPLETE"
            else:
                return "INVALID"

        # Reject additional content after the object
        elif state == "COMPLETE":
            return "INVALID"

    if state == "COMPLETE":
        try:
            json.loads(text)
        except json.JSONDecodeError:
            return "INVALID"

        return "COMPLETE"

    return "VALID_PREFIX"


if __name__ == "__main__":
    examples = [
        '{"name": 8}',
        '{"name": "Shrek",',
        '{"name": "Shrek",}',
        '{"name":}',
        '{"name":',
        '{"name": "Shrek", "city": "Lyon"}',
        '{"name": "Shrek"}Hello',
    ]

    for example in examples:
        status = classify_simple_object(example)

        print(f"Text: {repr(example)}")
        print(f"Status: {status}")
        print()
