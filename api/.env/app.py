from flask import Flask
from flask_smorest import Api
from sha256 import bl as bl
app=Flask(__name__)
app.config["PROPAGATE_EXPECTATIONS"]=True
app.config["API_TITLE"]="security tag"
app.config["API_VERSION"]="1.0"
app.config["OPENAPI_VERSION"]="3.0.3"
app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
api=Api(app)
api.register_blueprint(bl)
if __name__=="__main__":
    app.run(host="0.0.0.0",port=80,debug=False)