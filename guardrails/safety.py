def validate_input(input_text: str) -> str:
    """
    Validates the input to ensure it's not malicious or harmful.
    For now, it just checks if the input is empty.
    """
    if not input_text or not input_text.strip():
        return "Error: Input cannot be empty."
    return input_text.strip()

def validate_output(output: str) -> str:
    """
    Validates the output to ensure it's safe and appropriate.
    """
    return output.strip() if output and output.strip() else "Error: Empty response."