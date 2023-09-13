import os
from flask import Flask, request, jsonify, url_for

from sqlalchemy.sql import func

import uuid
from datetime import time, datetime

from database.db import db
from database.schema import Receipt, Item


receipts = {}
points = {}

'''
Setting up SQLite Database and Flask App
'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.create_all()


'''
Process Receipts Endpoint
TODO: Explain DB Logic
'''
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt_data = request.json

    #validate data

    #TODO test
    return jsonify({"success": receipt_data["retailer"]})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)