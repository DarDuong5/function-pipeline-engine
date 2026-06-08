from typing import Callable, Any, TypeVar
from time import perf_counter
import functools

logs = []

C = TypeVar('C', bound=Callable)

def timer(func: C) -> C:    
    """Timer decorator"""
    @functools.wraps(func)
    def get_time(*args: Any, **kwargs: Any) -> Any:
        """Purpose: Calls the given function and records the time taken to execute"""
        start = perf_counter() 
        result = func(*args, **kwargs)
        end = perf_counter()
        time = end - start
        name = func.__name__
        print(f'{name} ran for {time:.2f}s')
        return result
    return get_time

def logger(func: C) -> C:
    """Logger decorator"""
    @functools.wraps(func)
    def log_func(*args: Any, **kwargs: Any) -> Any:
        """Purpose: Logs the given function when executed."""
        parsed_args = ', '.join(repr(arg) for arg in args)
        parsed_kwargs = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        name = func.__name__
        if parsed_kwargs:
            parsed_func = f'{name}({parsed_args + ', ' + parsed_kwargs})'
        else:
            parsed_func = f'{name}({parsed_args})'
        print(f'Logged {parsed_func}')
        logs.append(parsed_func)
        return func(*args, **kwargs)
    
    return log_func




