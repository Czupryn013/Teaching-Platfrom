import yaml
import logging
import jsonpickle
import exceptions
from models import User, CensuredUser, Role
from extensions import db


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

logging.basicConfig(level=logging.INFO,filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

def add_user(username, password):
    user = User(username=username, password=password, role=Role.STUDENT.__str__())

    results = User.query.filter_by(username=username).all()
    if results: raise exceptions.UsernameTakenError()

    db.session.add(user)
    db.session.commit()

    logging.info(f"User {username} added")

def remove_user(id_to_delete):
    results = User.query.filter_by(id=id_to_delete).first()

    if not results: raise exceptions.UserDosentExistError()

    User.query.filter_by(id=id_to_delete).delete()
    db.session.commit()

    logging.info(f"User with id {id_to_delete} has been removed sucessfuly.")

def see_all_users():
    results = User.query.all()
    users = []
    for user in results: users.append(CensuredUser(user.id, user.username, user.role))

    return jsonpickle.encode(users, unpicklable=False)

def see_user_data(user_id):
    results = User.query.filter_by(id=user_id).first()

    if not results: raise exceptions.UserDosentExistError()

    user = CensuredUser(results.id, results.username, results.role)

    return jsonpickle.encode(user, unpicklable=False)


