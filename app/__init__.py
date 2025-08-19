from flask import Flask
USERS = []
app = Flask(__name__)

from app import views
from app import models