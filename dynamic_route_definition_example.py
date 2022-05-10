from fastapi import FastAPI
from starlette.responses import RedirectResponse
from types import CodeType, FunctionType
import uvicorn


def _add_route(app, path, message):
    test_code_str = f"""
def test(int_val, str_val):
    return {{
        "message": "{message}",
        "i": int_val,
        "s": str_val
    }}
"""

    test_compiled = compile(test_code_str, '<string>', 'exec')
    test_code = [c for c in test_compiled.co_consts if isinstance(c, CodeType)][0]
    test_func = FunctionType(test_code, globals(), "test")
    test_func.__annotations__ = {"int_val": int, "str_val": str}
    test_func.__defaults__ = ('abc',)  # counts backwards -- so only str_val gets a default

    app.get(path, response_model=dict[str, int | str])(test_func)


app = FastAPI()
_add_route(app, '/test', 'Hello World')


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """Redirect main page to API docs."""
    return RedirectResponse("/docs")


if __name__ == '__main__':
    uvicorn.run(app)
