from flask_smorest import Blueprint
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from firebase_admin import credentials, firestore,initialize_app
from flask import jsonify
from requests import request
bl=Blueprint("security",__name__)
import os
import json
a=[]
firebase_credentials_json = os.environ.get('CRED_JASON')
if not firebase_credentials_json:
    raise ValueError("Firebase credentials not found in environment variables")

cred = credentials.Certificate(json.loads(firebase_credentials_json))

initialize_app(cred)
db = firestore.client()  # Initialize Firestore or Realtime Database client
# Define your Blueprint
@bl.route("/user", methods=["GET"])
class security(MethodView):
    def post(self):
        # Extract UID from the query string
        uid = request.args.get("uid")
        timestamp = request.args.get("timestamp")

        if not uid:
            return jsonify({"error": "Missing UID"}), 400

        # Optionally store UID and timestamp in Firestore
        try:
            db.collection("uids").add({"uid": uid, "timestamp": timestamp})
        except Exception as e:
            return jsonify({"error": f"Failed to save data: {str(e)}"}), 500
        a.append(uid)
        return jsonify({
            "message": "UID received successfully",
            "uid": uid,
            "timestamp": timestamp
        }), 200
@bl.route("/check")
class check(MethodView):
    def get(self):
        return a[0]
