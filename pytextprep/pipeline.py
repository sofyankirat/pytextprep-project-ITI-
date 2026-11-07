from .registry import get_step
from .validation import validate_params

class Pipeline:

    def __init__(self, steps):

        self._steps = []

        for name, params in steps:
            params = dict(params or {})           # if the user make the params=None will be {}
            func = get_step(name)                 # fails here if the name is unknown
            validate_params(name, func, params)   # fails here if a parameter is wrong
            self._steps.append((name, func, params))

    @property
    def steps(self):
        return [(name, params) for name, _, params in self._steps]

    def transform(self, text, return_tokens=False):
        for _, func, params in self._steps:
            text = func(text, **params)
        if return_tokens:
            return text.split() 
        else:
            return text

    def transform_batch(self, texts):
        return [self.transform(t) for t in texts]

    def __repr__(self):
        parts = [f"{name}({params})" for name, params in self.steps]
        return "Pipeline([" + ", ".join(parts) + "])"