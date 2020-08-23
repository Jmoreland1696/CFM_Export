import sys
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, request

# Read in Cloud Credentials
firebase_key = os.environ['firebase_credentials'].replace("\\n","\n")
databaseURL = os.environ['firebase_url']

ENV_KEYS = {
	"type": "service_account",
	"project_id": os.environ["project_id"],
	"private_key_id": os.environ["private_key_id"],
	"private_key": os.environ["private_key"].replace("\\n", "\n"),
	"client_email": os.environ["client_email"],
	"client_id": os.environ["client_id"],
	"auth_uri": os.environ["auth_uri"],
	"token_uri": os.environ["token_uri"],
	"auth_provider_x509_cert_url": os.environ["auth_provider_x509_cert_url"],
	"client_x509_cert_url": os.environ["client_x509_cert_url"]
	}

# Connecting
cred = credentials.Certificate(ENV_KEYS)
firebase_admin.initialize_app(cred, {'databaseURL': databaseURL})

# Initialize App
app = Flask(__name__)

# Dashboard
@app.route('/')
def index():
	print('App was tested')
	sys.stdout.flush()
	return "Madden CFM Exporter V1.0"

# Clear DB
@app.route('/delete')
def delete():
	db.reference().delete()
	return "Data Cleared"

# Team Info
@app.route('/<system>/<leagueId>/leagueteams', methods=['POST'])
def teams(system,leagueId):
	db.reference('data/'+system+'/'+leagueId+'/leagueteams').set(request.json)
	return 'OK', 200

# Team Standings
@app.route('/<system>/<leagueId>/standings', methods=['POST'])
def standings(system,leagueId):
	db.reference('data/'+system+'/'+leagueId+'/standings').set(request.json)
	return 'OK', 200

# Free Agents
@app.route('/<system>/<leagueId>/freeagents/roster', methods=['POST'])
def freeagents(system, leagueId):
	db.reference('data/'+system+'/'+leagueId+'/freeagents').set(request.json)
	return 'OK', 200

# Rosters
@app.route('/<system>/<leagueId>/team/<teamId>/roster', methods=['POST'])
def roster(system, leagueId, teamId):
	db.reference('data/'+system+'/'+leagueId+'/team/'+teamId).set(request.json)
	return 'OK', 200

# Weekly stats
@app.route('/<system>/<leagueId>/week/<weekType>/<weekNumber>/<dataType>', methods=['POST'])
def stats(system, leagueId, weekType, weekNumber, dataType):
	statname = list(request.json.keys())[0]
	db.reference('data/'+system+'/'+leagueId+'/week/'+weekType+'/'+weekNumber+'/'+dataType+'/'+statname).set(request.json[statname])
	return 'OK', 200

if __name__ == '__main__':
	app.run()
