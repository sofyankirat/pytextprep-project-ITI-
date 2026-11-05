import functools

def requires_str(func):
    @functools.wraps(func)
    def wrapper(text, *args, **kwargs):
        if not isinstance(text, str):
            raise TypeError(f"expected str, got {type(text).__name__}")
        return func(text, *args, **kwargs)
    return wrapper