from flask import Flask

USERS = []
EXPRS = []
app = Flask(__name__)

from app import views
from app import models
