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