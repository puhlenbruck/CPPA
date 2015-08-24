from flask import Flask

from .auth import login_manager

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"
login_manager.init_app(app)

from .index import views
from .users import views


