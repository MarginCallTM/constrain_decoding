from llm_sdk import Small_LLM_Model

from src.file_handler import load_json_file
from src.models import FunctionDefinition, PromptInput
from src.prompting import build_prompt
import json


if __name__ == "__main__":
    # 1 - Load and validate the definitions
    raw_functions = load_json_file(
        "data/input/functions_definition.json"
    )

    functions = [
        FunctionDefinition.model_validate(item)
        for item in raw_functions
    ]

    # 2 - Load the first question
    raw_prompts = load_json_file(
        "data/input/function_calling_tests.json"
    )

    user_prompt = PromptInput.model_validate(
        raw_prompts[0]
    ).prompt

    # 3. Build the complete Prompt
    complete_prompt = build_prompt(
        user_prompt,
        functions
    )

    # 4. Load Qwen and encode the prompt
    model = Small_LLM_Model()
    input_ids = model.encode(complete_prompt).tolist()[0]

    generated_ids = []

    # 5. Generation without constraints.
    for _ in range(128):
        logits = model.get_logits_from_input_ids(input_ids)

        next_token_id = max(
            range(len(logits)),
            key=lambda token_id: logits[token_id]
        )

        input_ids.append(next_token_id)
        generated_ids.append(next_token_id)

    response = model.decode(generated_ids)

    print("\n--- TEST 1: json.load() ---")

    try:
        result = json.loads(response)
        print("Valid JSON:", result)
    except json.JSONDecodeError as exc:
        print("JSON PARSING FAILED", exc)

    print("\n --- TEST 2: raw_decode() ---")

    try:
        result, end_position = json.JSONDecoder().raw_decode(
            response.lstrip()
        )

        print("Parsed object:", result)
        print("End position:", end_position)

        remaining_text = response.lstrip()[end_position:]

        print("Remaining text:", repr(remaining_text[:60]))
    except json.JSONDecodeError as exc:
        print("JSON parsing failed", exc)

    # 6. Print ony the generated reply
    print("\nUSER REQUEST:")
    print(user_prompt)

    print("\nQWEN RESPONSE:")
    print(model.decode(generated_ids))
