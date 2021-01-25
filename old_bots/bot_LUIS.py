import json
from botbuilder.core import ActivityHandler, TurnContext, ConversationState, MessageFactory
from botbuilder.dialogs import DialogSet, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import PromptOptions, ConfirmPrompt, TextPrompt
from luis_manager import LUISRec
from SQL_manager import DBConnector


class MyBotLUIS(ActivityHandler):
    def __init__(self, conversation: ConversationState):
        self.luisReg = LUISRec()
        self.DBConnector = DBConnector()

        self.lastEntity = None

        self.con_state = conversation
        self.state_prop = self.con_state.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)

        # definiamo i diversi dialog
        self.dialog_set.add(ConfirmPrompt("interessato"))
        self.dialog_set.add(TextPrompt("testo"))

        # definiamo un dialog waterfall composto da diversi dialog ti dipo prompt
        self.dialog_set.add(WaterfallDialog("main_dialog", [self.get_confirmation_intrest,
                                                            self.update_intrest]))


    async def get_confirmation_intrest(self, waterfall_step: WaterfallStepContext) -> DialogTurnResult:
        appelli = self.DBConnector.get_appelli_esame(self.lastEntity)
        # waterfall_step.values["name"] = waterfall_step._turn_context.activity.text
        await waterfall_step.context.send_activity(appelli)

        return await waterfall_step.prompt(
            "interessato",
            PromptOptions(prompt=MessageFactory.text("Sei uno stidente interesato all'appello?")))

    async def update_intrest(self, waterfall_step: WaterfallStepContext):
        if waterfall_step.result:
            self.DBConnector.update_interesati(self.lastEntity)

        await waterfall_step.context.send_activity(MessageFactory.text("Grazie. Posso fare altro?."))
        return await waterfall_step.end_dialog()

    async def on_message_activity(self, turn_context: TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if dialog_context.active_dialog is not None:
            await dialog_context.continue_dialog()
        else:
            intent, luis_result = await self.luisReg.recog(turn_context)

            if luis_result is not None:
                #print("Intent trovato:", intent)
                entity, type = await self.luisReg.getEntities(luis_result)

                if intent == "esamiInVista":
                    # intent esamiInVista

                    if entity is None:
                        # print("Nesuna entità. Richiedi la lista di appelli a partire da oggi")
                        appelli = self.DBConnector.get_all_appelli()
                        await turn_context.send_activity(appelli)
                    else:
                        self.lastEntity = entity
                        #print("entità: ", entity, ", tipo: ", type)
                        if type == "builtin.datetimeV2.date":
                            json_str = json.loads((str(entity)).replace("'", "\""))
                            data = json_str.get('value')
                            appelli = self.DBConnector.get_all_appelli(data)
                            await turn_context.send_activity(appelli)
                        if type == "esame":
                            await dialog_context.begin_dialog("main_dialog")
                elif intent == "interessati":
                    self.lastEntity = entity
                    print("bello:", entity)
                    interessati = self.DBConnector.get_interessati(self.lastEntity)
                    await turn_context.send_activity(interessati)
            else:
                # No intent
                print("Nessun intent")

        # data la natura stateless del bot dobbiamo salare lo stato
        await self.con_state.save_changes(turn_context)


