#  ----------------- Custom Exceptions -----------------  #

class PyTextPrepError(Exception):
    """Base class for all PyTextPrep errors"""

class UnknownStepError(PyTextPrepError):
    """Raised when a step name is not registered"""

class InvalidStepParamsError(PyTextPrepError):
    """Raised when a step gets parameters it does not accept"""