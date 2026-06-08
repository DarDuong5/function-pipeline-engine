from decorators import timer, logger, logs
from strategies import errors
from pipeline import Pipeline

# First demo: Will raise an exception.
pipeline1 = Pipeline(strategy='fail_fast')
# Second demo: Will store errors but continue running calls with previous input.
pipeline2 = Pipeline(strategy='collect_errors')
# Third demo: Does not store errors but will skip the call with the error and continue next call with 
# previous input.
pipeline3 = Pipeline(strategy='skip_on_failure')

@timer
@logger
def normalize(text: str) -> str:
    """
    Purpose: Gets rid of extra whitespaces and every char becomes lowercase.
    """
    return text.strip().lower()

pipeline1.step(normalize)
pipeline2.step(normalize)
pipeline3.step(normalize)

@timer
@logger
def remove_punctuation(text: str) -> str:
    """
    Purpose: Removes special characters excluding whitespaces.
    """
    return ''.join(c for c in text if c.isalnum() or c.isspace())

pipeline1.step(remove_punctuation)
pipeline2.step(remove_punctuation)
pipeline3.step(remove_punctuation)

@timer
@logger
def broken_step(text: str) -> str:
    """
    Purpose: Implemented for didactic reason.
    """
    raise ValueError('Something went wrong!')

pipeline1.step(broken_step)
pipeline2.step(broken_step)
pipeline3.step(broken_step)

@timer
@logger
def tokenize(text: str) -> list[str]:
    """
    Purpose: Returns a list of substrings in the string.
    """
    return text.split()

pipeline1.step(tokenize)
pipeline2.step(tokenize)
pipeline3.step(tokenize)

def main():
    # RESULTS

    # result1 = pipeline1.run('  Hello, World!  ') # WILL FAIL
    # print(f'Logs: {logs}') # Cannot log here because we already had our first exception

    result2 = pipeline2.run('  Hello, World!  ')
    print(f'Result from pipeline2: {result2}')
    print(f'Errors from pipeline2: {errors}') 
    print(f'Logs from pipeline2: {logs}')

    errors.clear()
    logs.clear()

    result3 = pipeline3.run('  Hello, World!  ')
    print(f'Result from pipeline3: {result3}')
    print(f'Errors from pipeline3: {errors}') # We would've saw an errors here but none showed up
    print(f'Logs from pipeline3: {logs}') 

if __name__ == '__main__':
    main()






