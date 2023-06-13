from flask import Flask
from os import getenv
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
csrf = CSRFProtect(app)

import routes