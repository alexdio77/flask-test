import os
from flask import Flask


app = Flask(__name__)

app.debug = True
app.config["JWT_DEFAULT_REALM"] = os.getenv("JWT_DEFAULT_REALM")
