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

    >>> from googlespread.googlespread import GoogleSpread
    >>> google = GoogleSpread()
    >>> google.auth(secret_json = SECRET,
                    scope = SCOPE,
                    user_agent = USER_AGENT,
                    redirect_uri = REDIRECT_URI)

    >>> client = google.StartClient(spreadsheet = SPREADSHEET,
                                    worksheet = WORKSHEET)
