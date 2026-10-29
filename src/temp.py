import json

examples = [
    "42",
    "-3.14",
    "-",
    "3.",
    "3.5",
    "01",
    "3e-",
    "3e-2",
]

for text in examples:
    try:
        value = json.loads(text)
        print(f"{text!r:8} -> COMPLETE: {value}")
    except json.JSONDecodeError:
        print(f"{text!r:8} -> REJECTED")
