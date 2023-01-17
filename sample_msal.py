import json
import logging
import requests
import msal
import pprint

#"scope": ["https://graph.microsoft.com/.default"],

'''
Application (client) ID: e20c8713-e150-4ab2-b3e5-e7a29767d335
Directory (tenant) ID: fcb2b37b-5da0-466b-9b83-0014b67a7c78
Object ID: a80fe33b-ea42-4b69-bcc1-92c03832d514

CLIENT SECRETS
---------------
ID: a152a7b6-2f52-482b-b225-93ed05e9de3f
VALUE: 4mEM8cgc.2qcd7g4Q_ZHPjGOV~73_Vob6-
'''

config = {
    "authority": "https://login.microsoftonline.com/fcb2b37b-5da0-466b-9b83-0014b67a7c78",
    "client_id": "e20c8713-e150-4ab2-b3e5-e7a29767d335",
    "scope": ["https://graph.microsoft.com/.default"],
    "secret": "4mEM8cgc.2qcd7g4Q_ZHPjGOV~73_Vob6-",
    "endpoint": "https://graph.microsoft.com/v1.0/users/"
}

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"]
    )

result = None

result = app.acquire_token_silent(config["scope"], account=None)


if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])



# print("TOKEN RESULT: %s" % json.dumps(result, indent=2))


if "access_token" in result:
    graph_data = requests.get(
        config["endpoint"],
        headers={'Authorization': 'Bearer ' + result['access_token']},).json()
    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))

else:
    print("**************** error in sample ***********************")
    print(result.get("error"))
    print(result.get("error_description"))
    #print(result.get("correlation_id"))  # You may need this when reporting a bug
