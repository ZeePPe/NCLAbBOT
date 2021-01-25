from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState
import textwrap
import pyodbc



class MyBot_CSQLDB(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"You said something like '{turn_context.activity.text}'")

class Cosmo_manager:

    def __init__(self):
        _endpoint = 'https://nclab-db.documents.azure.com:443/'
        _key = "qNjGem3dNAeNa8kYuvfkQKvHAEA2nkMevzqtRCao9ckEQJrCGYbbPcuDL84nwDJb3kYz3jStQuPrWGtwrBZqRA=="
        _database_name = "nclab-db"
        _container_name = "container1"

    def query_database(self, query):
        pass


if __name__ == "__main__":
    print("as")

