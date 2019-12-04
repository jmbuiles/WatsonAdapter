from flask import Flask, request
from adaptadores.NewRelicAdapter import NewRelicAdapter

import requests
import os
import json

app = Flask(__name__)

port = os.getenv("PORT")
route_prefix='/'

NewRelicAdapter.register(app)

if port is None:
    port = 8080
else:
    port = int(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
