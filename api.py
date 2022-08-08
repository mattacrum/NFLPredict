from flask import Flask, request
import csv
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/")

class NFL_Teams(Resource):
    def get(self):

        nfl_team_stats = []

        with open('nfl_team_stats.csv', newline='') as csvfile:
            temp = csv.DictReader(csvfile)
            nfl_team_stats = list(temp)
        return jsonify(nfl_team_stats)

api.add_resource(NFL_Teams, '/nfl_teams')

if __name__ == '__main__':
   app.run(port=5002)
