from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
import simplejson as json

try:
    from flask.ext.cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS

app = Flask(__name__)
app.config.from_object("config")
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
db.create_all()


class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    happy = db.Column(db.Boolean)
    measure = db.Column(db.Float)


# One of the simplest configurations. Exposes all resources matching /api/* to
# CORS and allows the Content-Type header, which is necessary to POST JSON
# cross origin.
CORS(app, resources=r'/api/*', headers='Content-Type')

API_KEY = "3da541559918a808c2402bba5012f6c60b27661c"

@app.route("/api/v1/users", methods=['GET'])
def list_users():
    return jsonify({"results": [{"name": "anon"}]})


@app.route("/api/v1/log", methods=['POST'])
def post_log():
    if request.args.get("apikey") == API_KEY:
        args = request.args.copy()
        args.pop("apikey")
        log = Log(**args)
        db.session.add(log)
        db.session.commit()


@app.route("/api/v1/log", methods=['POST'])
def post_logs():
    if request.args.get("apikey") == API_KEY:
        log_data = json.loads(request.data)
        for args in log_data:
            log = Log(**args)
            db.session.add(log)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
