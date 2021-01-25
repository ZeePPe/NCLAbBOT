# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, ConversationState, MessageFactory
from botbuilder.dialogs import DialogSet, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, PromptOptions, PromptValidatorContext


class MyBotDialog(ActivityHandler):

    """Logica ad Dialog"""
    def __init__(self, conversation: ConversationState):
        self.con_state = conversation
        self.state_prop = self.con_state.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)
        #definiamo i diversi dialog
        self.dialog_set.add(TextPrompt("text_prompt"))
        self.dialog_set.add(NumberPrompt("number_prompt", self.is_valid_phone_number))
        # definiamo un dialog waterfall composto da diversi dialog ti dipo prompt
        self.dialog_set.add(WaterfallDialog("main_dialog", [self.get_user_name,
                                                            self.get_user_phone,
                                                            self.get_email,
                                                            self.completed]))

    # possiamo personalizzare la validazione di un messaggio inviao al bot,
    # controlliamo ad esempio la lunghezza del numero di telefono
    async def is_valid_phone_number(self, prompt_validator: PromptValidatorContext):
        if(prompt_validator.recognized.succeeded is False):
            await prompt_validator.context.send_activity("Please, enter a correct phone number")
            return False
        else:
            value = str(prompt_validator.recognized.value)
            if len(value) < 3 or len(value) > 15:
                await prompt_validator.context.send_activity("Please, enter a correct phone number")
                return False
        return True

    async def get_user_name(self, waterfall_step: WaterfallStepContext):
        return await waterfall_step.prompt("text_prompt",
                                           PromptOptions(prompt=MessageFactory.text("Please enter the name")))


    async def get_user_phone(self, waterfall_step: WaterfallStepContext):
        # possiamo salvare nel waterfall la risposta inserita dall'utente al turno precedente
        waterfall_step.values["name"] = waterfall_step._turn_context.activity.text

        return await waterfall_step.prompt("number_prompt",
                                           PromptOptions(prompt=MessageFactory.text("Please enter the phone number")))

    async def get_email(self, waterfall_step: WaterfallStepContext):
        waterfall_step.values["phone"] = waterfall_step._turn_context.activity.text
        return await waterfall_step.prompt("text_prompt",
                                           PromptOptions(prompt=MessageFactory.text("Please enter the E-mail")))

    async def completed (self, waterfall_step: WaterfallStepContext):
        waterfall_step.values["mail"] = waterfall_step._turn_context.activity.text

        # possiamo salvare tutte le info memorizzate durante il waterfall
        name = waterfall_step.values["name"]
        phone = waterfall_step.values["phone"]
        mail = waterfall_step.values["mail"]
        profile_info = f"name: {name}, phone: {phone}, mail: {mail}"
        await waterfall_step._turn_context.send_activity(profile_info)
        return await waterfall_step.end_dialog()

    # Ora definiamo il metodo on_turn per gestire le richieste
    async def on_turn(self, turn_context: TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if(dialog_context.active_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog("main_dialog")

        # data la natura stateless del bot dobbiamo salare lo stato 
        await self.con_state.save_changes(turn_context)
