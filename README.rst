googlespread
------------

Setup your project at the Google developer console:
    Start at https://console.developers.google.com/project
        - Create new project
            - Expand APIs & auth
                - Credentials
                    - Create new Client ID
                        - Web type
                            - Download JSON

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
