from typing import Any
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from types import CodeType, FunctionType
import uvicorn
from uuid import uuid4


def _add_route(app, path, message):
    # Define the function (annotations, defaults, and imports not needed as they are defined elsewhere
    test_code_str = f"""
def test(int_val, str_val):
    return {{
        "message": "{message}",
        "i": int_val,
        "s": str_val,
        "id": f"{{uuid4()}}"
    }}
"""

    # Compile the code
    test_compiled = compile(test_code_str, "<string>", "exec")

    # Find the code object that represents the function (this only works if there is exactly one function defined in the code, which will be the case)
    test_code = next(c for c in test_compiled.co_consts if isinstance(c, CodeType))

    # Define the globals, including imports
    globals_ = {"uuid4": uuid4}

    # Define the function defaults
    arg_defaults = ("abc",)  # counts backwards, so only str_val gets a default

    # Create the callable
    test_func = FunctionType(test_code, globals_, "test", arg_defaults)

    # Annotate the function arguments
    test_func.__annotations__ = {"int_val": int, "str_val": str, "return": dict[str, Any]}

    # Create the API route
    app.get(path, response_model=dict[str, Any])(test_func)


app = FastAPI()
_add_route(app, "/test", "Hello World")


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """Redirect main page to API docs."""
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app)
