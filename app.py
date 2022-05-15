from flask import Flask, request
from enum import Enum
app = Flask(__name__)


class Method:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@app.route("/user", methods=[Method.GET, Method.POST, Method.PUT])
def user():

    if request.method == Method.GET:
        return 'Getting a user'

    elif request.method == Method.POST:
        return

    elif request.method == Method.PUT:
        return

    elif request.method == Method.DELETE:
        return


@app.route("/note", methods=[Method.GET, Method.POST, Method.PUT])
def note():
    if request.method == Method.GET:
        return "Getting a note"

    elif request.method == Method.POST:
        return

    elif request.method == Method.PUT:
        return

    elif request.method == Method.DELETE:
        return


if __name__ == '__main__':
    app.run(debug=True)
