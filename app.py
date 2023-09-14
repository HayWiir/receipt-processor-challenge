import os
from flask import Flask, request, jsonify, url_for

from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

import uuid
from datetime import time, datetime

from model.db import db
from model.schema import Receipt, Item, init_db
from src.receipt_service import ReceiptService



'''
Setting up SQLite Database and Flask App
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# engine = create_engine(
#     "sqlite://", 
#     connect_args={"check_same_thread": False}, 
#     poolclass=StaticPool
# )


db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()


'''
Process Receipts Endpoint
This route does the following:
1. Get the input data in JSON format
2. Perform validation and raise exception in case of errors
3. Calculate points for valid data
4. Add data to SQLite DB
'''
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt_data = request.json
    receipt_service = ReceiptService(db)

    try:
        receipt_service.parse_receipt(receipt_data=receipt_data)
        receipt_id = receipt_service.add_receipt()
        points = receipt_service.calculate_points()

        return jsonify({"id": receipt_id, "points": points}), 200

    except Exception as e:
        return jsonify({"Error": f"{str(e)}"}), 400

'''
Get Points Endpoint
This route does the following:
1. Get the input receipt_id in JSON format
2. Check if receipt_id exists in DB
3. Return points calculated for the recipt or raise error if no receipt exists. 
'''
@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):

    receipt_service = ReceiptService(db)

    try:
        points = receipt_service.get_points(receipt_id)
        return jsonify({"points": points}), 200

    except Exception as e:
        return jsonify({"Error": f"{str(e)}"}), 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)