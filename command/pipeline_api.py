"""Trigger App to trigger execution of SAM Console (in Batch Mode)."""
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import os
import sys
import subprocess
import shutil

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    """Home function."""
    return "OK"

@app.route('/status', methods=['GET'])
def status():
    """Status function."""
    return "OK"

@app.route('/batch', methods=['POST'])
def batch():
    """Status function."""
    return "OK"    



app.run(host='0.0.0.0')