from .db import db
from sqlalchemy.orm import validates
import re

class Receipt(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    retailer = db.Column(db.Text, nullable=False)
    purchase_date = db.Column(db.Date(), nullable=False)
    purchase_time = db.Column(db.Time(), nullable=False)
    items = db.relationship('Item', backref='receipt', lazy=True)
    total = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Receipt {self.id} for {self.retailer}>'
    
    @validates('retailer')
    def validate_retailer(self, key, address):
        if not address or not re.match(r"^\S+$", address):
            raise ValueError("Failed retailer validation")
        return address
    
    @validates('total')
    def validate_total(self, key, address):
        if not address or not re.match(r"\d+\.\d{2}$", address):
            raise ValueError("Failed total validation")
        return address



class Item(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    receipt_id = db.Column(db.String(64), db.ForeignKey('receipt.id'), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Item {self.id} for Receipt {self.receipt_id}>'
    
    @validates('short_description')
    def validate_short_description(self, key, address):
        if not address or not re.match(r"^[\w\s\-]+$", address):
            raise ValueError("Failed shortDescription validation")
        return address
    
    @validates('price')
    def validate_price(self, key, address):
        if not address or not re.match(r"\d+\.\d{2}$", address):
            raise ValueError("Failed price validation")
        return address


def init_db():
    db.create_all()
