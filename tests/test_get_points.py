import json
import uuid

from tests.base_case import BaseCase


class TestGetReceipt(BaseCase):
    def test_random_receipt_id(self):
        #Test with an id that is not present
        random_uuid = str(uuid.uuid4())
        response = self.client.get(f"/receipts/{random_uuid}/points")
        self.assertEqual(404, response.status_code)

    def test_invalid_receipt_id(self):
        #Test with an id that is invalid
        random_uuid = "2144##"
        response = self.client.get(f"/receipts/{random_uuid}/points")
        self.assertEqual(404, response.status_code)    

    def test_successful_points1(self):
        payload = json.dumps(
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {
                        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                        "price": "12.00",
                    },
                ],
                "total": "35.35",
            }
        )

        response1 = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        id = response1.json["id"]

        response2 = self.client.get(f"/receipts/{id}/points")
        self.assertEqual(28, response2.json["points"])
        self.assertEqual(200, response2.status_code)

    def test_successful_points2(self):
        # The time is 15:01 which increases score by 10 points from previous test
        payload = json.dumps(
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "15:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {
                        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                        "price": "12.00",
                    },
                ],
                "total": "35.35",
            }
        )

        response1 = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        id = response1.json["id"]

        response2 = self.client.get(f"/receipts/{id}/points")
        self.assertEqual(38, response2.json["points"])
        self.assertEqual(200, response2.status_code)

    def test_successful_points3(self):
        # The day is even which reduces score by 6 points from previous test
        payload = json.dumps(
            {
                "retailer": "Target",
                "purchaseDate": "2022-01-04",
                "purchaseTime": "15:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {
                        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                        "price": "12.00",
                    },
                ],
                "total": "35.35",
            }
        )

        response1 = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        id = response1.json["id"]

        response2 = self.client.get(f"/receipts/{id}/points")
        self.assertEqual(32, response2.json["points"])
        self.assertEqual(200, response2.status_code)

    def test_successful_points4(self):
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

        response1 = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        id = response1.json["id"]

        response2 = self.client.get(f"/receipts/{id}/points")
        self.assertEqual(109, response2.json["points"])
        self.assertEqual(200, response2.status_code)

    def test_successful_points5(self):
        # Total is no longer a round integer reducing the score by 50 points from previous test
        payload = json.dumps(
            {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.50"},
                ],
                "total": "9.25",
            }
        )

        response1 = self.client.post(
            "receipts/process",
            headers={"Content-Type": "application/json"},
            data=payload,
        )

        id = response1.json["id"]

        response2 = self.client.get(f"/receipts/{id}/points")
        self.assertEqual(59, response2.json["points"])
        self.assertEqual(200, response2.status_code)
