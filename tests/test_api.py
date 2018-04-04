###########################################
# File: test_api.py
# Desc: some testing for the API
# Apr 2018
###########################################

import unittest
import json
from flask import url_for
from app import create_app, db
from app.models import Task

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_add_task(self):
        response = self.client.post(
            url_for('api.new_task'),
            headers = self.get_api_headers(),
            data = json.dumps({'description': 'test description'}),
            content_type='application/json')

        response = json.loads(response.get_data())
        self.assertTrue(response['description'] == 'test description')


    def test_search_task(self):
        response = self.client.get(
            url_for('api.get_tasks_by'),
            headers = self.get_api_headers(),
            query_string = dict(q = 'test description'),
            content_type = 'application/json')

        response = json.loads(response.get_data())
        self.assertTrue(response.status_code == 201)
