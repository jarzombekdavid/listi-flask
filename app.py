from flask import Flask
from apis import api

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
api.init_app(app)

app.run(debug=True)