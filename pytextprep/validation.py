import inspect
from .exceptions import InvalidStepParamsError
import functools

def requires_str(func):
    # functools.wraps copies the original function's name and docstring to wrapper
    # so the decorated function keeps its identity so for instance lowercase.__name__ stays "lowercase"
    @functools.wraps(func) 
    def wrapper(text, *args, **kwargs):
        if not isinstance(text, str):
            raise TypeError(f"expected str, got {type(text).__name__}")
        return func(text, *args, **kwargs)
    return wrapper

def validate_params(step_name, func, params):
    # names of the parameters of the step without the first one (text)
    allowed = list(inspect.signature(func).parameters)[1:]

    for key in params:
        if key not in allowed:
            raise InvalidStepParamsError(
                f"{step_name!r} got an unexpected parameter {key!r}. "
                f"Allowed parameters: {allowed}")