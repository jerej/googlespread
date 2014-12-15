googlespread
############

Simplify using oAuth2 to access Google Spreadsheets and provide easier access to selecting a spreadsheet/worksheet by-name as well ass for appending rows to the given worksheet.

StartClient() returns an oAuth authorized gdata client object which can be used directly with any gdata methods.

See the gdata python client for more info: https://code.google.com/p/gdata-python-client/
gdata python client wiki: https://code.google.com/p/gdata-python-client/w/list

Generating the oAuth2 data for your app
***************************************

Setup your project at the Google developer console:
    Start at https://console.developers.google.com/project
        - Create new project
            - Expand APIs & auth
                - Credentials
                    - Create new Client ID
                        - Web type
                            - Download JSON

Basic Usage
***********

To use simply do::

    >>> from googlespread import GoogleSpread
    >>> google = GoogleSpread()
    >>> google.auth(secret_json = SECRET,
                    scope = 'http://spreadsheets.google.com/feeds/',
                    user_agent = USER_AGENT,
                    redirect_uri = REDIRECT_URI)

    >>> client = google.StartClient(spreadsheet = "my spreadsheet",
                                    worksheet = "sheet2")

    >>> fields = {'timestamp': "This",
                  'temperature': "and",
                  'humidity': "That"}

    >>> result = google.AppendRow(fields)

Methods
*******

    def __init__(self, secret_json=None,
                 scope="",
                 redirect_uri="http://localhost",
                 user_agent="MyClient/1.0"):

    def auth(self, secret_json,
             scope="",
             redirect_uri="http://localhost",
             user_agent="MyClient/1.0"):

Setup the client connection to the correct worksheet and authorize it.
    def start_client(self,
                     spreadsheet=None, spreadsheet_id=None,
                     worksheet=None, worksheet_id=None):

Set/change the spreadsheet_id being used by the client using either the name or ID
    def set_spreadsheet(self,
                        spreadsheet=None, spreadsheet_id=None):

Set/channge the spreadsheet_id being used by the client using either the name or ID
    def set_worksheet(self,
                      spreadsheet=None, spreadsheet_id=None,
                      worksheet=None, worksheet_id=None):

Retrieve a spreadsheet's ID by its name
    def get_spreadsheet_id_by_name(self, spreadsheet):
        Returns:
            (string) spreadsheet-id

Retrieve a worksheet's ID given its name and either the name or ID of the parent spreadsheet
    def get_worksheet_id_by_name(self, worksheet, spreadsheet=None, spreadsheet_id=None):
        Returns:
            (string) worksheet-id

Simple method for appending a row to a worksheet
    def append_row(self, data):
        Append a row to a worksheet.

        Args:
            data (dict): The keys MUST be lowercase, alpha-only, and MUST be the first row of the worksheet.
        Returns:
            a gdata row object, if successful.
