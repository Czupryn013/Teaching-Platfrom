import yaml
from flask import Flask
from controller import controller_bp
from db_handler import handler_bp
from extensions import db
from models import User


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
db_config = config["database"]

app = Flask(__name__)
app.register_blueprint(controller_bp)
app.register_blueprint(handler_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_config['user']}:{db_config['password']}" \
                                        f"@localhost/{db_config['dbname']}"

db.init_app(app)
app.run()

db.create_all(bind_key="__all__")
