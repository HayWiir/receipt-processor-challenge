# from model.db import db
from model.schema import Receipt, Item, init_db

import uuid
from datetime import time, datetime

class ReceiptService:

    def  __init__(self, db):
        self.db = db
        self.retailer = None
        self.purchase_timestamp_str = None
        self.purchase_date = None
        self.purchase_time = None
        self.total = None
        self.items = []


    def parse_receipt(self, receipt_data):

        self.retailer = receipt_data['retailer']
        self.purchase_timestamp_str = f"{receipt_data['purchaseDate']}T{receipt_data['purchaseTime']}"
        
        try:
            self.purchase_timestamp = datetime.strptime(self.purchase_timestamp_str, '%Y-%m-%dT%H:%M')
        except ValueError:  
            raise ValueError("Failed purchaseTime/purchaseDate validation")
        
        self.purchase_date = self.purchase_timestamp.date() 
        self.purchase_time = self.purchase_timestamp.time()   
        self.total = receipt_data['total']
        
        self.items = []
        current_total = 0
        for item in receipt_data['items']:
            short_description = item['shortDescription']
            price = item['price']

            self.items.append({'short_description': short_description, 
                               'price': price})
            
            #Validate item prices with receipt total
            current_total += float(price) 

        if not self.items:
            raise ValueError("Failed items validation")  

        if current_total != float(self.total):
            raise ValueError("Inconsistency in items price and receipt total")  



    def add_receipt(self):
        self.receipt_id = str(uuid.uuid4())

        receipt = Receipt(id=self.receipt_id,
                           retailer=self.retailer,
                           purchase_date=self.purchase_date,
                           purchase_time=self.purchase_time,
                           total=self.total)  
        self.db.session.add(receipt)
        self.db.session.commit()

        for item in self.items:
            item_data = Item(id=str(uuid.uuid4()),
                        receipt_id=self.receipt_id,
                        short_description=item['short_description'], 
                        price=item['price'])
            
            self.db.session.add(item_data)
            self.db.session.commit()

        return self.receipt_id    
        
