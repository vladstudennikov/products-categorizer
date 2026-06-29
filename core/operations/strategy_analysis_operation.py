from core.abstractions.operation import BaseOperation
from core.abstractions.strategy_descriptor import BaseStrategyDescriptor
from core.context.pipeline_context import PipelineContext

class StrategyAnalysisOperation(BaseOperation):
    def __init__(self, descriptor: BaseStrategyDescriptor):
        self.descriptor = descriptor

    def run(self, context: PipelineContext) -> None:
        if not hasattr(context.state, 'strategy_report'):
            raise TypeError(
                "Context state does not support strategy_report. "
                "Please use StrategyPipelineState or a state with the 'strategy_report' field."
            )
        
        context.state.strategy_report = self.descriptor.analyze_strategy()
