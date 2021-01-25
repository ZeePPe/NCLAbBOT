# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from NCLabBot1.config import DefaultConfig


class MyBot_QnA(ActivityHandler):
    def __init__(self):
        qna_endpoint = QnAMakerEndpoint(DefaultConfig.qna_kb_id, DefaultConfig.qna_endpoint_key, DefaultConfig.qna_host)
        self.qnd_maker = QnAMaker(qna_endpoint)

    async def on_message_activity(self, turn_context: TurnContext):
        response = await self.qnd_maker.get_answers(turn_context)
        if response and len(response) > 0:
            await turn_context.send_activity(MessageFactory.text(response[0].answer))

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")