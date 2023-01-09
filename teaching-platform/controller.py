from flask import Blueprint
from flask import request

import db_handler
import exceptions


controller_bp = Blueprint("controller_bp", __name__)


@controller_bp.route("/users", methods=["POST"])
def add_user():
    try:
        request_data = request.get_json()
        username, password = request_data.get("username"), request_data.get("password")

        if not username or not password: return "Incorrect json body", 400
        db_handler.add_user(username, password)
        return f"User {username} has been added sucessfuly.", 201
    except (exceptions.UsernameTakenError,exceptions.PasswordToWeakError,exceptions.IncorrectUsername) as e:
        return e.message, e.status

@controller_bp.route("/users/<id_to_delete>", methods=["DELETE"])
def remove_user(id_to_delete):
    try:
        db_handler.remove_user(id_to_delete)
        return f"User with id {id_to_delete} has been deleted sucessfuly.", 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@controller_bp.route("/users", methods=["GET"])
def see_all_users():
    return db_handler.see_all_users(), 200

@controller_bp.route("/users/<user_id>", methods=["GET"])
def see_user_data(user_id):
    try:
        results = db_handler.see_user_data(user_id)
        return results, 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status


