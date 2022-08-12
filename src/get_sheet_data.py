import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

CREDENTIALS_FILE = 'src/creds.json'
spreadsheet_id = '1yWcBQDo2VxVFFWWaDPAF_fLM7mfu3gDWaifqwsVhVsU'


def get_sheet_data():
    credantials = ServiceAccountCredentials.from_json_keyfile_name \
            (
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
        )

    httpAuth = credantials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    table_data = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:D1000',
        majorDimension='ROWS'
    ).execute()
    return table_data


if __name__ == "__main__":
    get_sheet_data("")
