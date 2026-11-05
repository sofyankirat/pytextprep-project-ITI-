from .exceptions import UnknownStepError

STEPS = {}

# Registers a function in the STEPS dictionary under the given name
# Example: @register_step("lowercase") sets STEPS["lowercase"] = lowercase
def register_step(name):
    def decorator(func):
        STEPS[name] = func
        return func
    return decorator

# Looks up a function by its name and returns it
# Raises UnknownStepError if the name is not registered
def get_step(name):
    if name not in STEPS:
        raise UnknownStepError(f"{name!r} is not a step.")
    return STEPS[name]

# Returns the names of all registered steps, sorted alphabetically
def available_steps():
    return sorted(STEPS)