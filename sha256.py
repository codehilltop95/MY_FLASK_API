from flask_smorest import Blueprint
from flask.views import MethodView
from firebase_admin import credentials, firestore,initialize_app,auth,db,_apps
from flask import jsonify
from flask import request
from passlib.hash import pbkdf2_sha256
bl=Blueprint("security",__name__)
import os
firebase_credentials_json = os.environ.get('CRED_JSON')
j=_apps
if not j:
    cred = credentials.Certificate(firebase_credentials_json)
    initialize_app(cred)
@bl.route("/user", methods=["GET"])
class security(MethodView):
    def get(self):
        page = auth.list_users()
        latest_user = None

        # Get the most recently created user
        for user in page.users:
            if not latest_user or user.user_metadata.creation_timestamp > latest_user.user_metadata.creation_timestamp:
                latest_user = user
        uid_val=latest_user.uid
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
