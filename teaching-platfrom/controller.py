from flask import Flask
from flask import request
import db_handler



app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add_user():
    request_data = request.get_json()
    username, password = request_data.get("username"), request_data.get("password")

    if not username or not password: return "Incorrect json body", 400

    status = db_handler.add_user(username, password)

    if status == 409: return "Username alreday taken, pick a diffrent one", 409
    else: return request_data, 200

@app.route("/remove", methods=["DELETE"])
def remove_user():
    request_data = request.get_json()
    id_to_delete = request_data.get("id")

    if not id_to_delete: return "Incorrect json body.", 400

    status = db_handler.remove_user(id_to_delete)

    return f"User with id {id_to_delete} has been removed sucessfuly.", 200


@app.route("/users", methods=["GET"])
def see_all_users():
    return db_handler.see_all_users()

@app.route("/users/<user_id>", methods=["GET"])
def see_user_data(user_id):
    results = db_handler.see_user_data(user_id)
    if results == 400: return "This id dose not exist", 400
    else: return results[0], 200