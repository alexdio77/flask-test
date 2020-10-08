import os
from flask import request, jsonify
from app import app
from jwt_utils import jwt_required, current_identity


@app.route('/')
def home():
   return jsonify(
       message="hello world!",
       Authorization=request.headers.get('Authorization'),
       meta={
           'HOSTNAME': os.getenv('HOSTNAME'),
           'VERSION': os.getenv('VERSION'),
       }
    ), 200

@app.route('/protected')
@jwt_required(realm='pufin')
def protected():
   return jsonify(
    #    Authorization=request.headers.get('Authorization'),
       sub=current_identity.sub,
       jwt_payload=current_identity.payload,
       meta={
           'HOSTNAME': os.getenv('HOSTNAME'),
           'VERSION': os.getenv('VERSION'),
       }
    ), 200
