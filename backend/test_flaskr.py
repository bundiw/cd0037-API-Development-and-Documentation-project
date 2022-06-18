import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""


# DBNAME = trivia
# UNAME = postgres
# UPASS = password
# HOST = 127.0.0.1: 5432
# TEST_DBNAME = trivia_test

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('TEST_DBNAME')
        self.username = os.getenv('UNAME')
        self.password = os.getenv('UPASS')
        self.host = os.getenv('HOST')
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.username, self.password, self.host, self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/api/v1.0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_get_paginated_questions(self):
        res = self.client().get('/api/v1.0/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_success_post_questions(self):
        res = self.client().post('/api/v1.0/questions', json={
            "answer": "Barrack Obama",
            "category": 3,
            "difficulty": 1,
            "question": "Who was the president of US in 2015?"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_no_body_post_questions(self):
        res = self.client().post('/api/v1.0/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    def test_invalid_method_to_post_questions(self):
        res = self.client().post('/api/v1.0/questions', json={
            "answer": "Barrack Obama",
            "category": 3})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_success_get_categories(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_get_categories(self):
        res = self.client().get('/api/v1.0/categories/8')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_success_get_questions_by_categories(self):
        res = self.client().get('/api/v1.0/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['currentCategory'])

    def test_410_get_questions_by_categories(self):
        res = self.client().get('/api/v1.0/categories/8/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_success_search_questions(self):
        res = self.client().post('/api/v1.0/questions/search',
                                 json={"searchTerm": "m"})
        # http://localhost:5000/api/v1.0/questions/search
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_fail_search_questions(self):
        res = self.client().post('/api/v1.0/questions/search/r',
                                 json={"searchTerm": "mik"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_success_delete_question(self):
        res = self.client().delete("/api/v1.0/questions/18")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['success'], True)

    def test_fail_delete_question(self):
        res = self.client().delete("/api/v1.0/questions/100")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 410)
        self.assertTrue(data['message'])
        self.assertEqual(data['success'], False)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
