
from email import message
import json
from locale import currency
from logging import error
import os
from tkinter import FALSE
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1.0/categories')
    def retrieve_categories():
        categories = [category
                      for category in Category.query.all()]

        all_category = {
            str(category.id): category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': all_category
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/api/v1.0/questions')
    def retrieve_questions():
        error = False
        try:
            all_category = {}
            questions = [question for question in Question.query.all()]
            current_questions = paginate_questions(request, questions)

            if not current_questions:
                error = True
            else:
                categories = [category
                              for category in Category.query.all()]

                all_category = {
                    str(category.id): category.type for category in categories}

        except:

            error = True

        finally:
            if error:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(questions),
                    'categories': all_category,
                    'currentCategory': None
                })

    @app.route('/api/v1.0/questions', methods=['POST'])
    def create_question():
        error = False
        err = False
        try:
            res_question = request.get_json()

            # res_question.values()

            # question = Question(res_question['question'], res_question['answer'], res_question['category'],
            # res_question['difficulty'])
            # destructure the dictionary as constituent variables + val
            if res_question:
                try:
                    question = Question(**res_question)
                    question.insert()
                except:
                    err = True
                    error = False

            else:

                error = True
                err = False

        except:
            error = True

        finally:
            if error:
                abort(400)
            elif err:
                abort(422)
            else:

                return jsonify({
                    'success': True,
                    'created': question.format()
                })

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error = False
        try:
            question = Question.query.get(question_id)
            question.delete()
        except:
            error = True

        finally:
            if error:
                abort(410)
            else:
                return jsonify({
                    "deleted": question.format(),
                    "success": True
                }), 200

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/v1.0/questions/search', methods=['POST'])
    def search_question():

        # search_term = request.form.get('searchTerm', "")
        search_term = request.get_json()['searchTerm']

        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%'))
        match_questions = [question for question in questions]
        match_questions = paginate_questions(request, match_questions)
        if len(match_questions):

            return jsonify({
                "questions": match_questions,
                "success": True,
                "totalQuestions": len(match_questions),
                "currentCategory": None
            }), 200
        else:
            abort(404)

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def play_quizzes():

        # search_term = request.form.get('searchTerm', "")
        quiz_data = request.get_json()
        # print(quiz_data)
        currency_category = quiz_data['quiz_category']['id']
        # print(not currency_category.isdigit())
        if not currency_category.isdigit():
            abort(500)
        # {'previous_questions': [], 'quiz_category': {'type': 'History', 'id': '4'}}
        previous_questions = quiz_data['previous_questions']

        question = None
        questions = Question.query.filter_by(category=currency_category).all()
        for quis in questions:
            if quis.id in previous_questions:
                pass
            else:
                question = quis.format()
                break

        # print(question)

        if question:

            return question, 200
        else:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1.0/categories/<int:category>/questions')
    def retrieve_question_by_Category(category):
        error = False
        try:
            current_category = Category.query.get(category).type
        except:
            error = True
        finally:
            if error:
                abort(404)
            else:
                questions_by_category = Question.query.filter_by(
                    category=category).all()

                if questions_by_category:

                    questions = [
                        question for question in questions_by_category]
                    questions = paginate_questions(request, questions)
                    return jsonify({
                        "questions": questions,
                        "totalQuestions": len(questions),
                        "currentCategory": current_category,
                        "success": True

                    }), 200
                else:
                    abort(410)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def error_400(error):

        return jsonify({
            'success': False,
            'message': error.description,


        }), 400

    @app.errorhandler(410)
    def error_410(error):

        # print(dir(error))
        return jsonify({
            'success': False,
            'message': error.description,


        }), 410

    @app.errorhandler(404)
    def error_404(error):

        return jsonify({
            'success': False,
            'message': error.name,


        }), 404

    @app.errorhandler(405)
    def error_405(error):

        return jsonify({
            'success': False,
            'message': error.name,


        }), 405

    @app.errorhandler(422)
    def error_422(error):

        return jsonify({
            'success': False,
            'message': error.name,


        }), 422

    @app.errorhandler(500)
    def error_500(error):

        return jsonify({
            'success': False,
            'message': error.name,


        }), 500

    return app
