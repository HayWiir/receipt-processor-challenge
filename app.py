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
TODO: Explain DB Logic
'''
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt_data = request.json

    #validate data

    receipt_service = ReceiptService(db)

    try:
        receipt_service.parse_receipt(receipt_data=receipt_data)
        receipt_id = receipt_service.add_receipt()
        #calc points

        return jsonify({"id": receipt_id}), 200

    except Exception as e:
        return jsonify({"Error": f"{str(e)}"}), 400



    # receipt_id = str(uuid.uuid4())
    # retailer = receipt_data['retailer']
    # purchase_timestamp = f"{receipt_data['purchaseDate']}T{receipt_data['purchaseTime']}"
    # purchase_date = datetime.strptime(purchase_timestamp, '%Y-%m-%dT%H:%M').date()
    # purchase_time = datetime.strptime(purchase_timestamp, '%Y-%m-%dT%H:%M').time()
    # total = receipt_data['total']
    # items = receipt_data['items']

    # receipt = Receipt(id=receipt_id,
    #                        retailer=retailer,
    #                        purchase_date=purchase_date,
    #                        purchase_time=purchase_time,
    #                        total=total)  
    # db.session.add(receipt)
    # db.session.commit()  

    # for item in items:
    #     item_id = str(uuid.uuid4())
    #     short_description = item['shortDescription']
    #     price = item['price']

    #     item_data = Item(id=item_id,
    #                     receipt_id=receipt_id,
    #                     short_description=short_description, 
    #                     price=price)
        
    #     db.session.add(item_data)
    #     db.session.commit()

    





    #TODO test
    return jsonify({"success": receipt_data["retailer"]})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)