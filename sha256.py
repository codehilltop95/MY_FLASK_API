from flask_smorest import Blueprint
from flask.views import MethodView
from firebase_admin import credentials, firestore,initialize_app,auth,db
from flask import jsonify
from flask import request
import logging
logging.basicConfig(level=logging.INFO)
import os,json
from passlib.hash import pbkdf2_sha256
bl=Blueprint("security",__name__)
last_hashed_uid = None
cred_path = os.environ.get("CRED_JSON")
if not cred_path:
    raise ValueError("CRED_JSON environment variable not set!")
cred = credentials.Certificate(cred_path)
initialize_app(cred)
@bl.route("/user", methods=["GET"])
class security(MethodView):
    def get(self):
        global last_hashed_uid
        page = auth.list_users()
        latest_user = None

        # Get the most recently created user
        for user in page.users:
            if not latest_user or user.user_metadata.creation_timestamp > latest_user.user_metadata.creation_timestamp:
                latest_user = user
        uid_val=latest_user.uid
        uid = pbkdf2_sha256.hash(uid_val)
        last_hashed_uid = uid
        timestamp = request.args.get("timestamp")
        if not uid:
            return jsonify({"error": "Missing UID"}), 400
        data={
            "message": "UID received successfully",
            "uid": uid,
            "timestamp": timestamp
        }
        logging.info("The result %s",data)
        return uid, 200
@bl.route("/call",methods=["GET"])
class callapi(MethodView):
    def get(self):
        global last_hashed_uid
        return last_hashed_uid, 200