from types import CodeType, FunctionType
from typing import Any
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse


def _add_route(app: FastAPI, path: str, message: str) -> None:
    # Define the function (annotations, defaults, and imports not needed as they are defined
    # elsewhere)
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
    code = compile(test_code_str, "<string>", "exec")

    # Find the code object that represents the function (this only works if there is exactly one
    # function defined in the code, which will be the case)
    func_code = next(c for c in code.co_consts if isinstance(c, CodeType))

    # Define the globals, including imports
    globals_ = {"uuid4": uuid4}

    # Define the function argument defaults
    arg_defaults = ("abc",)  # counts backwards, so only str_val gets a default

    # Create the function
    func = FunctionType(func_code, globals_, "test", arg_defaults)

    # Annotate the function arguments on the function
    func.__annotations__ = {"int_val": int, "str_val": str, "return": dict[str, Any]}

    # Create the API route
    app.get(path, response_model=dict[str, Any])(func)


app = FastAPI()
_add_route(app, "/test", "Hello World")


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """Redirect main page to API docs."""
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app)
