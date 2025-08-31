__all__ = ("views", "models", "services", "dto", "adapter")

from flask import Flask

app = Flask(__name__)

from . import views, models, services, dto, adapter

