from langchain_core.tools import tool
import ast
import math

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression safely."""
    try:
        # Safely evaluate the expression using ast
        node = ast.parse(expression, mode='eval')

        # Define allowed functions and constants
        allowed_names = {'__builtins__': None, 'math': math}
        code = compile(node, '<string>', 'eval')
        result = eval(code, allowed_names)  # nosec B307

        return str(result)
    except Exception as e:
        return f"Error: {e}"