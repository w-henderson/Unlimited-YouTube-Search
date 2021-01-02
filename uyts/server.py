"""Classes and methods relating to hosting a UYTS API server."""

from .search import Search
from flask import Flask
from flask_cors import CORS, cross_origin
import json

class Server:
    """Class representing a basic UYTS API server."""

    def __init__(self,serverName="uyts-api",serverMessage="Server online",rawHTML=False):
        self.app = Flask(serverName)
        self.cors = CORS(self.app)
        self.app.config["CORS_HEADERS"] = "Content-Type"

        @self.app.route('/')
        @cross_origin()
        def mainPage():
            if rawHTML:
                return serverMessage
            else:
                return "<style>*{font-family:Arial}</style><font size=20 color=green>"+serverMessage+"</font><br>Powered by Unlimited YouTube Search<br>GitHub: <a href='https://github.com/w-henderson/Unlimited-YouTube-Search'>https://github.com/w-henderson/Unlimited-YouTube-Search</a>"
        
        @self.app.route('/api/<query>')
        @self.app.route('/api/<query>/<minResults>')
        @cross_origin()
        def api(query,minResults=0):
            search = Search(query,int(minResults))
            resultsJSON = []
            for result in search.results:
                resultsJSON.append(result.ToJSON())
            return json.dumps(resultsJSON)

    def run(self,host="0.0.0.0",port=80):
        """Run the Flask server so it can begin to respond to requests."""

        self.app.run(host,port)