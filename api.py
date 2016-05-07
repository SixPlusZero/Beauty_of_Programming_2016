from flask import Flask
from flask_restful import Resource, Api, reqparse
import subprocess
import json

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
        cgiResult = subprocess.Popen(["cgi-bin/cgi.py", str(id1), str(id2)],\
                stdout=subprocess.PIPE).communicate()[0]
        print "CGIResult: #" + cgiResult + "#"
        if not cgiResult.startswith("Error: "):
                return json.loads(cgiResult)
        else:
                return cgiResult

api.add_resource(BOPRequest, '/bop')

if __name__ == '__main__':
    app.run(debug=True, port=80)
