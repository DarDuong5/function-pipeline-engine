# Function Pipeline Engine
A lightweight, configurable data processing pipeline engine built in Python, inspired by ETL systems and API middleware patterns.

## Overview
The Function Pipeline Engine allows you to compose a sequence of transformation steps into a reusable pipeline. Each step is a plain function registered via a decorator, and the pipeline executes them in order — passing the output of one step as the input to the next.

## Features
- Register pipeline steps using `@pipeline.step` — an instance method decorator
- Three execution strategies for error handling:
    - `fail_fast` — stops immediately on the first error
    - `collect_errors` — runs all steps, collects errors, continues with previous data on failure
    - `skip_on_failure` — silently skips failed steps and continues with previous data
- Automatic timing and logging via `@timer` and `@logger` decorators
- Full type hints throughout using `TypeVar`, `Callable`, `Literal`, and `TypeAlias`
- Strategy dispatch table for clean, extensible strategy selection
- Strategy validation in `Pipeline.__init__` with helpful error messages
- Includes a test suite covering all strategies and edge cases

## Concepts Demonstrated
- First-class functions, higher-order functions, and dispatch tables
- Type hints with `TypeVar`, `Callable`, `Literal`, and `TypeAlias` 
- Decorators, closures, and `functools.wraps` 
- Strategy pattern and decorator registry with plain functions 

## Usage
```python
from pipeline import Pipeline

pipeline = Pipeline(strategy='fail_fast')

@pipeline.step
@timer
@logger
def normalize(text: str) -> str:
    return text.strip().lower()

@pipeline.step
@timer
@logger
def tokenize(text: str) -> list[str]:
    return text.split()

result = pipeline.run('  Hello, World!  ')
['hello', 'world']
```

## File Structure
```
pipeline/
    protocols.py    # Processable protocol — shared type definitions
    decorators.py   # @timer, @logger decorators
    strategies.py   # fail_fast, collect_errors, skip_on_failure
    pipeline.py     # Pipeline class
    demo.py         # Demo showing all features
    tests.py        # Test suite
```
