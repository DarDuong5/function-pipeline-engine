from typing import Mapping, TypeVar
from protocols import Processable

errors = []
T = TypeVar('T')

def fail_fast(func: Processable, data: T) -> T:
    """
    Purpose: Raises the first error from a given call and ends the entire pipeline call. 
    """
    try:
        return func(data)
    except Exception:
        raise

def collect_errors(func: Processable, data: T) -> T:
    """
    Purpose: Stores any errors any calls have in the pipeline but will continue running with previous data.
    """
    try:
        return func(data)
    except Exception as e:
        error = f'{func.__name__}({data}): {e}'
        errors.append(error)
        return data

def skip_on_failure(func: Processable, data: T) -> T:
    """
    Purpose: Skips calls with failures and continues running next calls with previous data.
    """
    try:
        return func(data)
    except Exception:
        return data

dispatch_table: Mapping = {'fail_fast': fail_fast,
                           'collect_errors': collect_errors,
                           'skip_on_failure': skip_on_failure,}