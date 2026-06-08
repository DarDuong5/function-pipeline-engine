from typing import Sequence, TypeVar, NoReturn

from pipeline import Pipeline
from strategies import dispatch_table, errors
from decorators import logger, timer, logs

S = TypeVar('S')

# What I'll be mainly be testing on: '   Hello, world!!    ' -> [6, 7]

@logger
@timer
def normalize(data: S) -> S:
    return data.lower().strip()

@logger
@timer
def tokenize(data: S) -> Sequence[S]:
    return data.split()

@logger
@timer
def broken(data: S) -> NoReturn:
    raise ValueError('Something went wrong here.')

@logger
@timer
def embbed(data: Sequence[str]) -> list[int]:
    return [len(w) for w in data]

def test_pipeline() -> None:
    """Normal pipline runs correctly."""

    pipeline_fail_fast = Pipeline('fail_fast')
    pipeline_fail_fast.step(normalize)
    pipeline_fail_fast.step(tokenize)
    pipeline_fail_fast.step(embbed)
    test_data = '   Hello, world!!    '

    assert len(pipeline_fail_fast) == 3
    assert len(logs) == 0
    result = pipeline_fail_fast.run(test_data)
    assert result == [6, 7]
    assert len(logs) == 3

def test_fail_fast() -> None:
    """fail_fast raises on broken step."""

    pipeline_fail_fast = Pipeline('fail_fast')
    pipeline_fail_fast.step(normalize)
    pipeline_fail_fast.step(tokenize)
    pipeline_fail_fast.step(broken)
    pipeline_fail_fast.step(embbed)
    test_data = '   Hello, world!!    '
    errors.clear()
    logs.clear()

    assert len(pipeline_fail_fast) == 4
    
    try:
        pipeline_fail_fast.run(test_data)
        assert False, 'Expected ValueError but no exception was raised'
    except ValueError:
        pass

def test_collect_errors() -> None:
    """collect_errors continues and stores errors."""

    pipeline_collect_errors = Pipeline('collect_errors')
    pipeline_collect_errors.step(normalize)
    pipeline_collect_errors.step(tokenize)
    pipeline_collect_errors.step(broken)
    pipeline_collect_errors.step(embbed)
    test_data = '   Hello, world!!    '
    errors.clear()
    logs.clear()

    assert len(pipeline_collect_errors) == 4
    assert len(logs) == 0
    assert len(errors) == 0
    result = pipeline_collect_errors.run(test_data)
    assert result == [6, 7]
    assert len(errors) == 1
    assert len(logs) == 4

def test_skip_on_failure() -> None:
    """skin_on_failure skips and continues."""

    pipeline_skip_on_failure = Pipeline('skip_on_failure')
    pipeline_skip_on_failure.step(normalize)
    pipeline_skip_on_failure.step(tokenize)
    pipeline_skip_on_failure.step(broken)
    pipeline_skip_on_failure.step(embbed)
    test_data = '   Hello, world!!    '
    errors.clear()
    logs.clear()

    assert len(pipeline_skip_on_failure) == 4
    assert len(logs) == 0
    assert len(errors) == 0
    result = pipeline_skip_on_failure.run(test_data)
    assert result == [6, 7]
    assert len(logs) == 4
    assert len(errors) == 0

def test_invalid_strategy() -> None:
    """Invalid strategy raises ValueError."""

    try:
        invalid_pipeline = Pipeline('unknown')
        assert False, 'Expected ValueError but no exception was raised'
    except ValueError:
        pass

def test_empty_pipeline() -> None:
    """Empty pipeline returns input unchanged."""

    empty_pipeline = Pipeline('collect_errors')
    test_data = '   Hello, world!!    '
    errors.clear()
    logs.clear()

    assert len(logs) == 0
    assert len(errors) == 0
    result = empty_pipeline.run(test_data)
    assert result == test_data
    assert len(logs) == 0
    assert len(errors) == 0


