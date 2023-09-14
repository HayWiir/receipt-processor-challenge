from model.schema import Receipt, Item, init_db

import uuid
from datetime import time, datetime
import math


class ReceiptService:
    """
    Initialized with SQLAlchemy object for DB access
    """

    def __init__(self, db):
        self.db = db
        self.retailer = None
        self.purchase_timestamp_str = None
        self.purchase_date = None
        self.purchase_time = None
        self.total = None
        self.items = []
        self.points = 0

    """
    Parses and validates input JSON receipt data.
    """

    def parse_receipt(self, receipt_data):
        self.retailer = receipt_data["retailer"]
        self.purchase_timestamp_str = (
            f"{receipt_data['purchaseDate']}T{receipt_data['purchaseTime']}"
        )

        try:
            self.purchase_timestamp = datetime.strptime(
                self.purchase_timestamp_str, "%Y-%m-%dT%H:%M"
            )
        except ValueError:
            raise ValueError("Failed purchaseTime/purchaseDate validation")

        self.purchase_date = self.purchase_timestamp.date()
        self.purchase_time = self.purchase_timestamp.time()
        self.total = receipt_data["total"]

        self.items = []
        prices_list = []
        for item in receipt_data["items"]:
            short_description = item["shortDescription"]
            price = item["price"]

            self.items.append({"short_description": short_description, "price": price})

            # Validate item prices with receipt total
            prices_list.append(float(price))

        if not self.items:
            raise ValueError("Failed items validation")

        if math.fsum(prices_list) != float(self.total):
            raise ValueError("Inconsistency in items price and receipt total")

    """
    Adds data to SQLite DB.
    Raises errors in case of DB validation errors.
    """

    def add_receipt(self):
        self.receipt_id = str(uuid.uuid4())

        receipt = Receipt(
            id=self.receipt_id,
            retailer=self.retailer,
            purchase_date=self.purchase_date,
            purchase_time=self.purchase_time,
            total=self.total,
        )
        self.db.session.add(receipt)
        self.db.session.commit()

        for item in self.items:
            item_data = Item(
                id=str(uuid.uuid4()),
                receipt_id=self.receipt_id,
                short_description=item["short_description"],
                price=item["price"],
            )

            self.db.session.add(item_data)
            self.db.session.commit()

        return self.receipt_id

    """
    Calculates points to award based on rules
    """

    def calculate_points(self):
        # Retailer Name
        self.points += sum(c.isalnum() for c in self.retailer)

        # Round Dollar Amount
        self.points += 50 if float(self.total).is_integer() else 0

        # Multiple of 0.25
        self.points += 25 if float(self.total) % 0.25 == 0 else 0

        # Pair items
        self.points += (len(self.items) // 2) * 5

        # Trimmed length of item description
        for item in self.items:
            short_description_trimmed_len = len(item["short_description"].strip())
            if short_description_trimmed_len % 3 == 0:
                self.points += math.ceil(float(item["price"]) * 0.2)

        # Purchase day is odd
        self.points += 6 if self.purchase_timestamp.day % 2 != 0 else 0

        # If purchase between 14:00 and 16:00
        self.points += 10 if time(14) < self.purchase_timestamp.time() < time(16) else 0

        receipt = Receipt.query.filter_by(id=self.receipt_id).first()
        receipt.points = self.points
        self.db.session.commit()

        return self.points

    """
    Gets points for provided receipt_id (if exits in DB)
    """

    def get_points(self, receipt_id):
        self.receipt_id = receipt_id
        receipt = Receipt.query.filter_by(id=self.receipt_id).first()
        if receipt:
            return receipt.points
        else:
            raise ValueError("receipt_id does not exist")
