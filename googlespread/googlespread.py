"""GoogleSpread - Access Google Spreadsheets API.

This module is to simplify access to certain portions of the Google Spreadsheet
APIs.

"""

#from pprint import pprint
import gdata.docs.service
import gdata.spreadsheets.client
import gdata.spreadsheets.data
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

class GoogleSpread(object):
    """Make it easier to access the Google Spreadsheet API

    """


    def __init__(self, secret_json=None,
                 scope="",
                 redirect_uri="http://localhost",
                 user_agent="MyClient/1.0"):
        self.secret_json = secret_json
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.user_agent = user_agent

        self.credential_store = 'googleplus.dat'

        # Just initialize for later
        self.authtoken = None
        self.client = None

        self.spreadsheet = None
        self.spreadsheet_id = None
        self.worksheet = None
        self.worksheet_id = None

    def auth(self, secret_json, scope="", redirect_uri="http://localhost",
             user_agent="MyClient/1.0"):
        """authenticate with OAuth2 to Google

        """
        self.secret_json = secret_json
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.user_agent = user_agent

        flow = flow_from_clientsecrets(self.secret_json,
                                       scope=self.scope,
                                       redirect_uri=redirect_uri)

        #auth_uri = flow.step1_get_authorize_url()

        storage = Storage(self.credential_store)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run(flow, storage)

        auth2token = gdata.gauth.OAuth2Token(client_id=credentials.client_id,
                                             client_secret=credentials.client_secret,
                                             scope=self.scope,
                                             access_token=credentials.access_token,
                                             refresh_token=credentials.refresh_token,
                                             user_agent=self.user_agent)
        self.authtoken = auth2token

    Auth = auth

    def start_client(self,
                     spreadsheet=None, spreadsheet_id=None,
                     worksheet=None, worksheet_id=None):
        """Setup the client connection to the correct worksheet and authorize
        it.

        Args:
            spreadsheet (str): Exact spreadsheet name
            spreadsheet_id (str): Spreadsheet ID (last part of SS URI)
            workdsheet (str): Exact worksheet name
            worksheet_id (str): Worksheet ID (last part of WS URI)

        Returns:
            (str): gdata client object

        Examples:
            client = google.StartClient()

            client = google.StartClient(spreadsheet_id = SPREADSHEET_ID,
                                        worksheet_id = WORKSHEET_ID)

            client = google.StartClient(spreadsheet_id = SPREADSHEET_ID)

            client = google.StartClient(spreadsheet = SPREADSHEET,
                                        worksheet = WORKSHEET)

        """
        self.client = gdata.spreadsheets.client.SpreadsheetsClient()
        self.authtoken.authorize(self.client)

        if spreadsheet:
            self.spreadsheet = spreadsheet
            if not spreadsheet_id:
                spreadsheet_id = self.GetSpreadsheetByName(spreadsheet)

        if spreadsheet:
            self.spreadsheet_id = spreadsheet_id

        if worksheet:
            self.worksheet = worksheet
            if not worksheet_id:
                worksheet_id = self.GetWorksheetByName(worksheet)

        if worksheet_id:
            self.worksheet_id = worksheet_id

        return self.client

    StartClient = start_client

    def set_spreadsheet(self,
                        spreadsheet=None, spreadsheet_id=None):
        """Setup the client connection to the correct worksheet and authorize
        it.

        Example:
            SPREADSHEET_ID = google.GetSpreadsheetByName(SPREADSHEET)
            google.SetSpreadsheet(spreadsheet_id = SPREADSHEET_ID)

        """
        if not spreadsheet_id:
            if not spreadsheet:
                raise SyntaxError("MUST provide one of spreadsheet or spreadsheet_id")

            else:
                spreadsheet_id = self.GetSpreadsheetByName(spreadsheet)

        if spreadsheet:
            self.spreadsheet = spreadsheet
        self.spreadsheet_id = spreadsheet_id

    SetSpreadsheet = set_spreadsheet

    def set_worksheet(self,
                      spreadsheet=None, spreadsheet_id=None,
                      worksheet=None, worksheet_id=None):
        """Setup the client connection to the correct worksheet and authorize
        it.

        Example:
            WORKSHEET_ID = google.GetWorksheetByName(WORKSHEET)
            google.SetWorksheet(worksheet_id = WORKSHEET_ID)

        """

        if not worksheet_id:
            if not worksheet:
                # Raise: MUST provide one of worksheet or worksheet_id
                raise SyntaxError("MUST provide one of worksheet or worksheet_id")

            else:
                worksheet_id = self.GetWorksheetByName(worksheet)

        if spreadsheet:
            self.spreadsheet = spreadsheet
        if spreadsheet_id:
            self.spreadsheet_id = spreadsheet_id
        if worksheet:
            self.worksheet = worksheet
        self.worksheet_id = worksheet_id

    SetWorksheet = set_worksheet

    def get_worksheet_id_by_name(self, worksheet, spreadsheet=None, spreadsheet_id=None):
        """Get a worksheet's ID

        """
        if not spreadsheet and not spreadsheet_id:
            spreadsheet = self.spreadsheet
            spreadsheet_id = self.spreadsheet_id

        if not self.client:
            # Should raise exception that no client connection is yet available.
            raise RuntimeError("gdata client connection not established")

        worksheet_id = None
        worksheets = self.client.GetWorksheets(spreadsheet_id)
        #pprint(worksheets.__dict__)
        for entry in worksheets.entry:
            #print "\n--- Sheet: ---"
            if worksheet == entry.title.text:
                #print entry.title.text
                #print entry.id.text
                worksheet_id =  entry.id.text.split('/')[-1]
                #print "WS_ID: %s" % worksheet_id

                #pprint(entry.id.__dict__)

        return worksheet_id

    GetWorksheetByName =  get_worksheet_id_by_name

    def get_spreadsheet_id_by_name(self, spreadsheet):
        """Get a spreadsheet's ID

        """
        if not self.client:
            # Should raise exception that no client connection is yet available.
            raise RuntimeError("gdata client connection not established")

        spreadsheet_id = None
        documents_feed = self.client.GetSpreadsheets()
        # Loop through the feed and extract each document entry.
        for document_entry in documents_feed.entry:
            # Display the title of the document on the command line.
            if document_entry.title.text == spreadsheet:
                #        print document_entry.title.text
                #print document_entry.id.text
                spreadsheet_id =  document_entry.id.text.split('/')[-1]
                #print "SS_ID: %s" % spreadsheet_id
                #        pprint(document_entry.id.__dict__)
                #        pprint(document_entry)

        return spreadsheet_id

    GetSpreadsheetByName = get_spreadsheet_id_by_name

    def append_row(self, data):
        """Append a row to a worksheet.

        Args:
            data (dict): The keys MUST be lowercase, alpha-only, and MUST be
            from the first row of the worksheet per Google API.

        Returns:
            (object): The return-value from client.AddListEntry() which is the
            row-data, if successful.

        """

        row = gdata.spreadsheets.data.ListEntry()
        row.from_dict(data)
        retval = self.client.AddListEntry(row, self.spreadsheet_id,
                                          self.worksheet_id)
        return retval

    AppendRow = append_row

