from .search import Search
from flask import Flask
from flask_cors import CORS, cross_origin
import json

class Server:
    def __init__(self):
        self.app = Flask("uyts-api")
        self.cors = CORS(self.app)
        self.app.config["CORS_HEADERS"] = "Content-Type"

        @self.app.route('/')
        @cross_origin()
        def mainPage():
            return "Server online"
        
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
        self.app.run(host,port)