import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@Done implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        query_drinks = Drink.query.all()
        drinks_list = [drink.short() for drink in query_drinks]
        print("hello")
        return jsonify({
            'success':True,
            'drinks':drinks_list
            }), 200
    except:
        abort(401)



'''
@Done implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        query_drinks = Drink.query.all()
        drinks_list = [drink.long() for drink in query_drinks]
        return jsonify({
            'success':True,
            'drinks':drinks_list
            }), 200
    except:
        abort(401)


'''
@Done implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    body = request.get_json()
    drink_title = body.get('title', None)
    drink_recipe = body.get('recipe', None)
    try:
        drink = Drink(title=drink_title, recipe=drink_recipe)
        drink.insert()
        query_drinks = Drink.query.all()
        drinks_list = [drink.long() for drink in query_drinks]
        return jsonify({
            'success':True,
            'drinks':drinks_list
            }), 200
    except:
        abort(401)

'''
@Done implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/int:<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    body = request.get_json()
    drink = Drink.query.get_or_404(drink_id)
    if drink == 404:
        abort(404)
    try:
        drink.title = body.get('title')
        drink.recipe = body.get('recipe')
        drink.update()
        return jsonify({
            'success':True,
            'drinks':drinks_list
            }), 200
    except:
        abort(401)



'''
@Done implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/int:<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.get_or_404(drink_id)
    if drink == 404:
        abort(404)

    try:
        drink.delete()
    except:
        abort(401)




# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@Done implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@Done implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({
            "success": False, 
            "error": 404, 
            "message": "ressource not found"
            }),404,
    )


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


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

'''
@Done implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
