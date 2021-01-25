from botbuilder.core import TurnContext
from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
import json
from NCLabBot1.config import DefaultConfig


class LUISServiceHandler:
    def __init__(self):
        luis_app = LuisApplication(DefaultConfig.LUIS_APPID, DefaultConfig.LUIS_PRIMARYKEY, DefaultConfig.LUIS_ENDPOINTURL)
        luis_option = LuisPredictionOptions(include_all_intents=True, include_instance_data=True)
        self.luisReg = LuisRecognizer(luis_app, luis_option, True)

    async def recog(self, turn_context: TurnContext):
        luis_result = await self.luisReg.recognize(turn_context)

        intent = LuisRecognizer.top_intent(luis_result, "None", DefaultConfig.LUIS_MIN_SCORE)

        if intent == "None":
            return None, None
        else:
            return intent, luis_result

    async def getEntities(self, luis_result):
        result = luis_result.properties["luisResult"]

        if len(result.entities) > 0:
            json_str = json.loads((str(result.entities[0])).replace("'", "\""))

            write_entity = json_str.get('entity')
            entity = json_str.get('additional_properties').get('resolution').get('values')
            type = json_str.get('type')

            return entity[0], type
        else:
            # Nessuna entità trovata
            return None, None
