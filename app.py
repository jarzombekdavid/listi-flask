from flask import Flask, request, g
from apis import api
from apis.auth import authenticate
#from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
#app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret_key'

api.init_app(app)

#CORS(app)

@app.after_request
def after_request(response):
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
  response.status = 'OK'
  response.status_code = 200
  return response

@app.before_request
def pre_request_authentication():
    g.user_id = authenticate()

# app.run(debug=True)