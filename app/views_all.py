from flask import Response

from app import app, USERS, QUESTIONS, EXPRS


@app.route("/")
def index():
    return Response(
        f"USERS:<br>{'<br>'.join(map(str, USERS))}<br>QUESTIONS:<br>{'<br>'.join(map(str, QUESTIONS))}<br>EXPRS:<br>{'<br>'.join(map(str, EXPRS))}"
    )
