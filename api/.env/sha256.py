from flask_smorest import Blueprint
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from firebase_admin import credentials, firestore,initialize_app
from flask import jsonify
from requests import request
bl=Blueprint("security",__name__)
cred = credentials.Certificate(r"C:\Users\HOME\Desktop\api\.env\fir-auth-cb338-firebase-adminsdk-qwk97-fa554685e7.json")  # replace with your downloaded JSON file path
initialize_app(cred)
db = firestore.client()  # Initialize Firestore or Realtime Database client
# Define your Blueprint
@bl.route("/call")
class security(MethodView):
    def get(self):
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

        return jsonify({
            "message": "UID received successfully",
            "uid": uid,
            "timestamp": timestamp
        }), 200