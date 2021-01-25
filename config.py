#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    #APP_ID = "1d88a938-5d23-4b1d-be78-3de6c2b4b552"
    #APP_PASSWORD = "958651a8-e241-4694-bd2b-f313daaeed1c"

    # Qna Service
    qna_kb_id = "d7455fd5-8cee-4347-9776-1052088341df"
    qna_endpoint_key = "e432e21e-9d8a-433c-8bcd-909a0280db8f"
    qna_host = "https://qnaservice2-asd.azurewebsites.net/qnamaker"

    # LUIS
    LUIS_APPID = "63fda683-a5f5-4ada-8847-acebd51de00b"
    LUIS_PRIMARYKEY = "08a8181a2006451e80a6d52c6f75f4b7"
    LUIS_ENDPOINTURL = "https://westeurope.api.cognitive.microsoft.com/"
    LUIS_MIN_SCORE = 0.90

    # SQL Service
    SQL_DRIVER = '{ODBC Driver 17 for SQL Server}'
    SQL_SERVER_NAME = 'nclab-server'
    SQL_DATABASE_NAME = 'nclab_db'
    SQL_SERVER = '{server_name}.database.windows.net,1433'.format(server_name=SQL_SERVER_NAME)
    SQL_USERNAME = "zeeppe"
    SQL_PASSWORD = "DeviAnceRuleZf79"

