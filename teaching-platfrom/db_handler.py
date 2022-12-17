import yaml
import psycopg2
import logging
from flask import Flask
import jsonpickle
from flask import request

with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
logging.basicConfig(level=logging.INFO,filemode="w", filename="../logs.log")

def get_connection_to_db():
    db_config = config["database"]
    conn = psycopg2.connect(host=db_config["host"],dbname = db_config["dbname"],
                            user = db_config["user"], port = db_config["port"], password = db_config["password"]
    )
    return conn

class User:
    def __init__(self, id, username, password="-"):
        self.id = id
        self.username = username
        self.password = password

app = Flask(__name__)
@app.route("/add", methods=["POST"])
def add_user():
    request_data = request.get_json()
    username, password = request_data.get("username"), request_data.get("password")
    conn = get_connection_to_db()
    cur = conn.cursor()
    if not username or not password: conn.close(); return "Incorrect json body", 422

    cur.execute("SELECT username FROM users")
    results = cur.fetchall()
    if (username,) in results:
        logging.warning("Username alreday taken, pick a diffrent one")
        conn.close()
        return "Username alreday taken, pick a diffrent one", 200

    query = f"INSERT INTO users (username, password,role) VALUES ('{username}', '{password}','USER')"
    cur.execute(query)
    conn.commit()
    logging.info(f"User {username} added")

    conn.close()
    return request_data, 200


def remove_user(username):
    conn = get_connection_to_db()
    cur = conn.cursor()

    query = f"DELETE FROM users WHERE username='{username}' "
    cur.execute(query)
    conn.commit()
    logging.info(f"User {username} removed")

    conn.close()

@app.route("/users", methods=["GET"])
def see_all_users():
    conn = get_connection_to_db()
    cur = conn.cursor()

    query = f"SELECT id,username FROM users"
    cur.execute(query)
    results = cur.fetchall()
    users = []

    for row in results:
        users.append(User(row[0], row[1]))
    conn.close()
    return jsonpickle.encode(users, unpicklable=False)

