#!/usr/bin/python
from flask import Flask
from flask_restful import Resource, Api, reqparse
import subprocess
import json
import main

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id1', type=int)
parser.add_argument('id2', type=int)

class BOPRequest(Resource):
    def get(self):
        args = parser.parse_args()
        id1 = args['id1']
        id2 = args['id2'] 
        print "id1@\t", id1
        print "id2@\t", id2
        cgiResult = main.request(id1, id2)
        print "CGIResult: #" + str(cgiResult) + "#"
        #if type(cgiResult) != type(""):
        #    return json.dumps(cgiResult)
        #else:
        #    return cgiResult
        return cgiResult

api.add_resource(BOPRequest, '/bop')

if __name__ == '__main__':
    app.run(debug=True, port=27016)
