import os
import logging
import redis
import gevent
import simplejson as json

from dateutil import parser as dateParser

from flask import Flask, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_sockets import Sockets

try:
    from flask.ext.cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS

REDIS_URL = os.environ['REDISCLOUD_URL']
REDIS_CHAN = 'rbft'

app = Flask(__name__)
app.config.from_object("config")
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
db.create_all()

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)


class ChatBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)

chats = ChatBackend()
chats.start()


class Log(db.Model):
    __tablename__ = '_rbft_log_'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    happy = db.Column(db.Boolean)
    measure = db.Column(db.Float)

# One of the simplest configurations. Exposes all resources matching /api/* to
# CORS and allows the Content-Type header, which is necessary to POST JSON
# cross origin.
CORS(app, resources={r"/api/*": {'origins': '*'}}, headers="Content-Type")

API_KEY = "3da541559918a808c2402bba5012f6c60b27661c"


@app.route('/')
def hello():
    return render_template('index.html')


@app.route("/api/v1/users", methods=['GET'])
def list_users():
    return jsonify({"results": [{"name": "anon"}]})


@sockets.route('/submit')
def inbox(ws):
    """Receives incoming chat messages, inserts them into Redis."""
    while ws.socket is not None:
        # Sleep to prevent *contstant* context-switches.
        gevent.sleep(0.1)
        message = ws.receive()

        if message:
            app.logger.info(u'Inserting message: {}'.format(message))
            redis.publish(REDIS_CHAN, message)


@sockets.route('/receive')
def outbox(ws):
    """Sends outgoing chat messages, via `ChatBackend`."""
    chats.register(ws)

    while ws.socket is not None:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep()


@app.route("/api/v1/log", methods=['POST'])
def post_log():
    if request.args.get("apikey") == API_KEY:
        args = json.loads(request.data)
        args['timestamp'] = dateParser \
            .parse(args['timestamp']) \
            .replace(tzinfo=None)
        log = Log(**args)
        db.session.add(log)
        db.session.commit()
    return jsonify({"results": [{"name": "anon"}]})


@app.route("/api/v1/log", methods=['POST'])
def post_logs():
    if request.args.get("apikey") == API_KEY:
        log_data = json.loads(request.data)
        for args in log_data:
            args['timestamp'] = dateParser \
                .parse(args['timestamp']) \
                .replace(tzinfo=None)
            log = Log(**args)
            db.session.add(log)
        db.session.commit()
    return jsonify({"results": [{"name": "anon"}]})
