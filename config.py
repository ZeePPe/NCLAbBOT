#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    
    # Qna Service
    qna_kb_id = "-----"
    qna_endpoint_key = "-----"
    qna_host = "https://qnaservice2-asd.azurewebsites.net/qnamaker"

    # LUIS
    LUIS_APPID = "-----"
    LUIS_PRIMARYKEY = "-----"
    LUIS_ENDPOINTURL = "https://westeurope.api.cognitive.microsoft.com/"
    LUIS_MIN_SCORE = 0.90

    # SQL Service
    SQL_DRIVER = '{ODBC Driver 17 for SQL Server}'
    SQL_SERVER_NAME = 'nclab-server'
    SQL_DATABASE_NAME = 'nclab_db'
    SQL_SERVER = '{server_name}.database.windows.net,1433'.format(server_name=SQL_SERVER_NAME)
    SQL_USERNAME = "zeeppe"
    SQL_PASSWORD = "-----"

