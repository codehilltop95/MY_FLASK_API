from flask_smorest import Blueprint
from flask.views import MethodView
from firebase_admin import credentials, firestore,initialize_app,auth,db
from flask import jsonify
from flask import request
from passlib.hash import pbkdf2_sha256
bl=Blueprint("security",__name__)
import os
import json
with open("findbuddy-2b5ed-firebase-adminsdk-fbsvc-00f944f8ad.json") as f:
    cred = credentials.Certificate(json.load(f))
initialize_app(cred,{
    'databaseURL': 'https://f-buddy-24b0b-default-rtdb.firebaseio.com/'  # Replace with your DB URL
})
db = firestore.client()
uuid=None
@bl.route("/user", methods=["GET"])
class security(MethodView):
    def get(self):
        global uuid
        ref = db.reference('/')  # adjust this to point to the right path if needed
        data = ref.get()
        if not data or "User UID" not in data:
            return jsonify({"error": "'User UID' not found in Firebase DB"}), 404
        uid_val=data["User UID"]
        uid = pbkdf2_sha256.hash(uid_val)
        timestamp = request.args.get("timestamp")
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
            "message":"UID fetched successfully" }),200
