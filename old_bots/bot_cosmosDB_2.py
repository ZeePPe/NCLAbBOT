from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState
#from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.cosmos.cosmos_client import CosmosClient
import json


class MyBot_CosmosDB(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"You said something like '{turn_context.activity.text}'")

class Cosmo_manager:

    def __init__(self):
        _endpoint = 'https://nclab-db.documents.azure.com:443/'
        _key = "qNjGem3dNAeNa8kYuvfkQKvHAEA2nkMevzqtRCao9ckEQJrCGYbbPcuDL84nwDJb3kYz3jStQuPrWGtwrBZqRA=="
        _database_name = "nclab-db"
        _container_name = "container1"
        self.client = CosmosClient(_endpoint, _key)
        self.database = self.client.get_database_client(_database_name)
        self.container = self.database.get_container_client(_container_name)

    def read_database(self, id):
        self.database = self.client.get_database_client(id)

        print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id,  self.database.database_link))

    def query_database(self, query):
        for item in self.container.query_items(
                query='SELECT * FROM products p WHERE p.productModel <> "DISCONTINUED"',
                enable_cross_partition_query=True,
        ):
            print(json.dumps(item, indent=True))


if __name__ == "__main__":
    print("as")
    cosm = Cosmo_manager()
    cosm.query_database("asd")
