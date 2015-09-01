from flask import Flask
import config
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_pyfile('../config.py')
CsrfProtect(app)
from .index import views
from .users import views, models
from .characters import views
from .auth import login_manager
login_manager.init_app(app)




