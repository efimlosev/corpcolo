# GitHub example


class PassPm:
    def __init__(self):
        self.url =  "https://provision.needaserver.net/jsonrpc.php"  # The Url of your provistion system
        self.headers = {'content-type': 'application/json'}
        self.auth = ('admin', 'passwod') # your login information
