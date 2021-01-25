from config import DefaultConfig
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from botbuilder.core import TurnContext


class QnAServiceHandler:
    def __init__(self):
        qna_endpoint = QnAMakerEndpoint(DefaultConfig.qna_kb_id,
                                         DefaultConfig.qna_endpoint_key,
                                         DefaultConfig.qna_host)
        self.qnd_maker = QnAMaker(qna_endpoint)

    async def get_response(self, turn_context: TurnContext):
        return await self.qnd_maker.get_answers(turn_context)
