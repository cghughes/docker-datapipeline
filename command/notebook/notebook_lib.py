"""Python lib to run Juptyer Notebooks."""
import requests
from shutil import Error
from websocket import create_connection, WebSocket, ABNF, WebSocketApp
import logging as log
import json

class Notebook:
    """Notebook management class for setting up the connection to Jupyter and handling the events."""

    headers = {'Content-Type': 'application/json'}

    session = None
    notebook_path = None
    base_url = None
    ws_url = None
    notebook_password = None

    cookie = None

    notebook_session_id = None
    active_kernel_id = None

    code = []

    def __init__(self, notebook_path, notebook_password = '3point142', base_url = 'localhost:8888'):
        """__init__ function."""
        self.base_url = 'http://' + base_url
        self.ws_url = 'ws://' + base_url
        self.notebook_path = notebook_path
        self.notebook_password = notebook_password

    def start_session(self):
        """Start_session function."""
        self.session = requests.Session()
        return self.session

    def login(self):
        """Login function."""
        if (self.session == None):
            raise Exception('No session set')

        response = self.session.request("GET", url=self.base_url + "/login")
        cookie=response.headers['set-cookie'].split(';')[0]
        self.cookie=cookie.split('=')[1]

        auth_payload = "password=" + self.notebook_password + "&_xsrf=" + self.cookie
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.session.request("POST", url=self.base_url + "/login", data=auth_payload, headers=headers)
        if (response.status_code == 200):
            print("Authenticated with _xsrf tag " + cookie)
            return True
        else:
            raise Exception("Authentication failed with " + response.status_code + " : " + response.content)
    
    def start_kernel(self):
        """Start_kernel function."""
        if (self.cookie == None):
            raise Exception('No cookie set from login')
        
        url = self.base_url + '/api/sessions?_xsrf=' + self.cookie
        payload = json.dumps({'name': '', 'path':self.notebook_path, 'type': 'notebook'})        
        response = self.session.request("POST", url=url, data=payload, headers=self.headers)
        kernel = json.loads(response.text)
        self.active_kernel_id = kernel['kernel']["id"]
        self.notebook_session_id = kernel["id"]        
        print("Kernel Started " + self.active_kernel_id)

    def build_notebook(self):
        """Build_notebook function."""
        if (self.cookie == None):
            raise Exception('No cookie set from login')
        
        url = self.base_url + '/api/contents' + self.notebook_path
        response = self.session.request("GET", url=url, headers=self.headers)
        notebook = json.loads(response.text)
        self.code = []
        for c in notebook['content']['cells']:    
            if len(c['source']) > 0:
                source = c['source']
                #print("Executing : " + source[:50])
                self.code.append(source)