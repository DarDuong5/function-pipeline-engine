from typing import Any, Literal
from strategies import dispatch_table
from protocols import Processable

StrategyLiteral = Literal['fail_fast', 'collect_errors', 'skip_on_failure']



class Pipeline:
    def __init__(self, strategy: StrategyLiteral) -> None:
        if strategy not in dispatch_table:
            raise ValueError(f'Unknown strategy: {strategy}. Choose from {list(dispatch_table.keys())}')
        self.calls = []
        self.strategy = strategy

    def __len__(self):
        return len(self.calls)
    
    def __repr__(self):
        return f'<Pipeline(calls: {self.calls}, strategy: {self.strategy})>'

    def step(self, func: Processable) -> Processable:
        """
        Instance method decorator
        Purpose: Appends given function object onto the call pipeline.
        """
        self.calls.append(func)
        return func
        
    def run(self, text: str) -> Any:
        """
        Purpose: Runs the functions in the call pipeline.
        """
        curr = text
        for c in self.calls:
            curr = dispatch_table[self.strategy](c, curr)
        return curr



