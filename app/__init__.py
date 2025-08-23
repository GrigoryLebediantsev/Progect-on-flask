from flask import Flask

USERS = []
EXPRS = []
QUESTIONS = []
app = Flask(__name__)

from app import views
from app import models
from app import views_all
