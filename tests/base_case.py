import unittest
import json

from app import app
from model.db import db, initialize_db


class BaseCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = db
        with self.app_context:
            self.db.create_all()

        # with app.app_context():
        #     self.db.create_all()

    def tearDown(self):
        with self.app_context:
            self.db.drop_all()
        self.app_context.pop()
