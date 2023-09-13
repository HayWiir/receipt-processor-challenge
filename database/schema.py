from .db import db

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    retailer = db.Column(db.Text, nullable=False)
    purchaseDate = db.Column(db.Date(), nullable=False)
    purchaseTime = db.Column(db.Time(), nullable=False)
    items = db.relationship('Item', backref='receipt', lazy=True)
    total = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Receipt {self.id} for {self.retailer}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Item {self.id} for Receipt {self.receipt_id}>'
