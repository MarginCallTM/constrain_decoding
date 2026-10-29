import json


def load_json_file(path: str) -> list[dict[str, object]]:
    try:
        with open(path, "r", encoding="utf-8") as document:
            data = json.load(document)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    return data


if __name__ == "__main__":
    data = load_json_file(
        "data/input/function_calling_tests.json"
    )

    print(type(data))
    print(len(data))
    print(data[0])
