import json

from tests.base_case import BaseCase


class TestGetReceipt(BaseCase):
    def test_successful_receipt(self):
        payload = json.dumps(
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            }
        )

        response = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(str, type(response.json["id"]))
        self.assertEqual(200, response.status_code)

    def test_receipt_wrong_retailer(self):
        payload = json.dumps(
            {
                "retailer": "",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            }
        )

        response = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        self.assertEqual(400, response.status_code)

    def test_receipt_wrong_datetime(self):
        payload = json.dumps(
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "20 March 2022",
                "purchaseTime": "02:33 PM",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            }
        )

        response = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(400, response.status_code)

    def test_receipt_wrong_desciption(self):
        payload = json.dumps(
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "9.00",
            }
        )

        response = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(400, response.status_code)

    def test_receipt_conflicting_price_total(self):
        # The total of item prices does not match receipt total
        payload = json.dumps(
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                ],
                "total": "7.00",
            }
        )

        response = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(400, response.status_code)

    def test_receipt_empty_items(self):
        # The total of item prices does not match receipt total
        payload = json.dumps(
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [],
                "total": "9.00",
            }
        )

        response = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(400, response.status_code)
