import yaml
import psycopg2
import logging
import jsonpickle
import exceptions
from models import User, CensuredUser, Role


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
logging.basicConfig(level=logging.INFO,filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

def get_connection_to_db():
    db_config = config["database"]
    conn = psycopg2.connect(host=db_config["host"],dbname = db_config["dbname"],
                            user = db_config["user"], port = db_config["port"], password = db_config["password"]
    )
    return conn

def add_user(username, password):
    conn = get_connection_to_db()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users")
    results = cur.fetchall()
    if (username,) in results:
        logging.warning("Username alreday taken, pick a diffrent one")
        conn.close()
        raise exceptions.UsernameTakenError()

    query = f"INSERT INTO users (username, password,role) VALUES ('{username}', '{password}','USER')"
    cur.execute(query)
    conn.commit()
    logging.info(f"User {username} added")

    conn.close()
    return 200

def remove_user(id_to_delete):
    conn = get_connection_to_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users")
    results = cur.fetchall()
    if (int(id_to_delete),) not in results:
        conn.close()
        raise exceptions.UserDosentExistError()

    query = f"DELETE FROM users WHERE id='{id_to_delete}'"

    cur.execute(query)
    conn.commit()
    logging.info(f"User with id {id_to_delete} has been removed sucessfuly.")

    conn.close()
    return 200

def see_all_users():
    conn = get_connection_to_db()
    cur = conn.cursor()

    query = f"SELECT id,username FROM users"
    cur.execute(query)
    results = cur.fetchall()
    users = []

    for row in results:
        users.append(CensuredUser(row[0], row[1]))

    conn.close()
    return jsonpickle.encode(users, unpicklable=False), 200

def see_user_data(user_id):
    conn = get_connection_to_db()
    cur = conn.cursor()

    query = f"SELECT id,username FROM users WHERE id = {user_id}"
    cur.execute(query)
    results = cur.fetchone()
    if not results: conn.close(); raise exceptions.UserDosentExistError()

    user = CensuredUser(results[0], results[1])
    conn.close()
    return jsonpickle.encode(user, unpicklable=False)


