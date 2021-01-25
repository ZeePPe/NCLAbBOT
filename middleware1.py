from botbuilder.core import Middleware, TurnContext
from typing import Callable, Awaitable
from botbuilder.schema import ActivityTypes


class Middleware1(Middleware):
    async def on_turn(self, turn_context: TurnContext, next:Callable[[TurnContext], Awaitable]):
        if turn_context.activity.type == ActivityTypes.message:
            # in questa sezione il codice verrà eseguito prima dell'esecuzione del bot
            await turn_context.send_activity("hey, i'm  middleware1!")

            await next()

            # in questa sezione, dopo next, il codice verrà eseguito dpo il bot
            await turn_context.send_activity("hey, i'm  middleware1 after the bot!")
        else:
            await next()
