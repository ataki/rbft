from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

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


@app.route("/api/v1/users", methods=['GET'])
def list_users():
    return jsonify({"results": [{"name": "anon"}]})


if __name__ == "__main__":
    app.run(debug=True)
