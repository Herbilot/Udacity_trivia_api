import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(
    DB_USER, DB_PASSWORD, "localhost:5432", DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.question = {
        "question":"do you like programming?",
        "answer":"yes",
        "Category":"1",
        "difficulty":"1"
        }

        self.search = {"search":"search_term"}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test get categories
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    #test request categories with an invalid id number
    def test_404_invalid_id_for_categories(self):
        res = self.client().get("/categories/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource not found")

    # test get questions
    def test_get_question(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # test requesting question to an invalid page number
    def test_404_invalid_page_number_for_question(self):
        res = self.client().get("/questions?page=50")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    #test request question by id
    def test_404_invalid_id_for_questions(self):
        res = self.client().get("/questions/544")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    #test delete question
    def test_delete_question(self):
        res = self.client().delete("/questions/11")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_question"], 11)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])

    #test delete a question that does not exist
    def test_404_question_does_not_exist(self):
        res = self.client().delete("/questions/1500")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #test adding new question
    def test_add_new_question(self):
        res = self.client().post("/questions", json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["new_question"])
        

    #test adding questions not allowed
    def test_405_adding_questions_not_allowed(self):
        res = self.client().post("/questions/50", json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    

    #test search found
    def test_search_found(self):
        res = self.client().post("/questions", json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    #test search not found
    def test_search_not_found(self):
        res = self.client().post("/questions", json={"searchTerm":"zazazazazazazaza"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['total_questions'],0)

    #test get question based on category
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["category"],"Art")
        self.assertEqual(data["success"], True)

    #test requesting questions in the category that does not exist
    def test_404_category_does_not_exist(self):
        res = self.client().get("/categories/200/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"],"ressource not found")
        self.assertEqual(data["success"], False)

    #test get quizz
    def test_get_quiz(self):
        res = self.client().post('/quizzes',json={'quiz_category':{'type':'Art','id':2},'previous_questions':[2,4]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])

    #test quizz failed
    def test_422_get_quiz(self):
        res = self.client().post('/quizzes',json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],"unprocessable")

    

        

   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()