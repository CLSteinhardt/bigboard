from pprint import pprint
from oauth2client import file, client, tools
from googleapiclient import discovery
from googleapiclient.discovery import build
from httplib2 import Http


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))
    
service = discovery.build('sheets', 'v4', credentials=creds)

spreadsheet_body = {
    # TODO: Add desired entries to the request body.
}

request = service.spreadsheets().create(body=spreadsheet_body)
response = request.execute()

# TODO: Change code below to process the `response` dict:
pprint(response)
