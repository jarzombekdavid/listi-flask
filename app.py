from flask import Flask, request, g
from apis import api
from apis.auth import authenticate

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
api.init_app(app)

@app.before_request
def pre_request_authentication():
    g.user_id = authenticate()

app.run(debug=True)