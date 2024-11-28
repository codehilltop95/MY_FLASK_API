from flask_smorest import Blueprint
from flask.views import MethodView
from firebase_admin import credentials, firestore,initialize_app
from flask import jsonify
from flask import request
from passlib.hash import pbkdf2_sha256
bl=Blueprint("security",__name__)
import os
import json
firebase_credentials_json = os.environ.get('CRED_JASON')
if not firebase_credentials_json:
    raise ValueError("Firebase credentials not found in environment variables")
cred = credentials.Certificate(json.loads(firebase_credentials_json))
initialize_app(cred)
db = firestore.client()  # Initialize Firestore or Realtime Database client
# Define your Blueprint
uuid=None
@bl.route("/user", methods=["GET"])
class security(MethodView):
    def get(self):
        # Extract UID from the query string
        uid = pbkdf2_sha256.hash(request.args.get("uid"))
        timestamp = request.args.get("timestamp")
        uuid=uid
        if not uid:
            return jsonify({"error": "Missing UID"}), 400
        return jsonify({
            "message": "UID received successfully",
            "uid": uid,
            "timestamp": timestamp
        }), 200
@bl.route("/call",methods=["GET"])
class callapi(MethodView):
    def get(self):
        return jsonify({
            "uid":uuid,
            "message":"UID fetched successfully" }),200
