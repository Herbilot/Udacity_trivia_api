import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from random import randrange
import collections


from models import setup_db, Question, Category

collections.Callable = collections.abc.Callable
collections.Iterable = collections.abc.Iterable

#const that defines number of question per page
QUESTIONS_PER_PAGE = 10

def pagination(request, questions_query):
    '''paginates question per page'''
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions_query]
    current_questions = questions[start:end]

    return current_questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @Done: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, ressources={r" /api/*": {"origin": "*"}})

    """
    @Done: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @Done:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        query_categories = Category.query.order_by(Category.id).all()
        Categories_list = {
        category.id:category.type for category in query_categories
        }



        return jsonify({
                'success':True,
                'categories': Categories_list

                })

    """
    @Done:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions_query = Question.query.order_by(Question.category).all()
        current_questions = pagination(request, questions_query)
        query_categories = Category.query.order_by(Category.id).all()
        Categories_list = {
        category.id:category.type for category in query_categories
        }

        if len(current_questions) == 0:
            abort(404)

        

        return jsonify({
            'success':True,
            'questions':current_questions,
            'total_questions':len(questions_query),
            'categories':Categories_list
            })

    

    """
    @Done:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)

            if question == 404:
                abort(404)

            question.delete()
            questions_query = Question.query.order_by(Question.category).all()
            current_questions = pagination(request, questions_query)

            return jsonify({
                'success':True,
                'questions':current_questions,
                'total_questions':len(questions_query),
                'deleted_question':question.id,
                })
        except:
            abort(422)


    """
    @Done:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        '''add question if the search term is not provide and search for question there is a search term'''
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        search = body.get("searchTerm", None)

        try:
            if search:
                search_question = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
                current_questions = pagination(request, search_question)

                return jsonify({
                        'success':True,
                        'questions':current_questions,
                        'total_questions':len(search_question.all())
                        })

            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                questions_query = Question.query.order_by(Question.id).all()
                current_questions = pagination(request, questions_query)

                return jsonify({
                    'success':True,
                    'questions':current_questions,
                    'new_question':question.id,
                    'total_questions':len(questions_query)
                    })
        except:
            abort(422)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        category = Category.query.get_or_404(category_id)

        if category is None:
            abort(404)

        try:
            questions = Question.query.filter_by(category=category.id).all()
            current_questions = pagination(request, questions)

            return jsonify({
                'success':True,
                'questions':current_questions,
                'total_questions':len(questions),
                'category':category.type
                })
        except:
            abort(400)

    """
    @Done:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def paly_quizz():
        try:
          cat=request.json.get('quiz_category',None)
          prev_questions=request.json.get('previous_questions',None)
          
          if (cat['id'] ==0):
            questions_av = Question.query.filter(Question.id.notin_((prev_questions))).all()

          else:
            questions_av = Question.query.filter_by(category=cat['id']).filter(Question.id.notin_((prev_questions))).all()
          
          if len(questions_av)>0:
            number_of_av_questions = len(questions_av)
            upcomming_questions=questions_av[randrange(0, number_of_av_questions)].format() 
          else:
            upcomming_questions = None
          
          if ((cat is None) or (prev_questions is None)):
            abort(404)

          return jsonify({
            'success':True,
            'question':upcomming_questions
            })
        except:
          abort(422)
    

    """
    @Done:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "ressource not found"
                }),404,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"
                }),405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": 
                "unprocessable"}),422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": "internal server error"
                }),500,
        )


    return app

