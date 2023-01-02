from flask import Flask
from controller import controller_bp


app = Flask(__name__)
app.register_blueprint(controller_bp)

app.run()

