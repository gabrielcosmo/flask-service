from flask import Flask, request, make_response, jsonify
import json
from db.operators import *
from db.models.models import UserConfig, NoteConfig

app = Flask(__name__)


class Method:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@app.route("/user", methods=[Method.POST, Method.PUT, Method.DELETE])
def user():
    if request.method == Method.POST:
        try:
            _req = request.get_json()
            _email = request.args['email']
            _pw = request.args['password']

        # caso o email ou a senha não sejam fornecidos
        except:
            return make_response(jsonify({"messege": "fail"}))

        else:
            try:
                # com valores para email e senha, procura-se o usuário
                _user = select_user(_email)
                # se validados, usuário e senha, e retornado os dados deste
                if _pw == _user.password:
                    response = make_response(
                        jsonify({
                            "id": _user.id,
                            "name": _user.name,
                            "email": _user.email,
                            "password": _user.password,
                            "emailsec": _user.emailsec,
                            "record": _user.record
                        })
                    )
                    response.headers["content-type"] = "application/json"
                    response.headers["status"] = "200 OK"
                    return response

            # senão encontrado, um novo usário tentará ser cadastrado
            except:
                try:
                    insert_user(request.args["name"], _email, _pw)

                # obrigatoriamente, deve-se informar um nome para o usário, caso não é lançada uma exceção
                except:
                    return jsonify({"messege": "'name' not found during user criation"})


    elif request.method == Method.PUT:
        try:
            _req = request.get_json()
            _email = _req["email"]
            _pw = _req["password"]
            _user = select_user(_email)

        except:
            return make_response(jsonify({"messege": "fail"}))

        else:
            if _user.password == _pw:
                _req_dict = json.loads(_req)
                fields = []

                for k in _req_dict.keys():
                    fields.append(k)

                if UserConfig.NAME in fields:
                    if _req_dict[fields] != _user.name: update_user(_email, UserConfig.NAME, _req_dict["name"])

                elif UserConfig.EMAIL in fields:
                    if _req_dict[fields] != _user.email: update_user(_email, UserConfig.EMAIL, _req_dict["email"])

                elif UserConfig.PASSWORD in fields:
                    if _req_dict[fields] != _user.password: update_user(_email, UserConfig.PASSWORD, _req_dict["password"])

                elif UserConfig.EMAILSEC in fields:
                    if _req_dict[fields] != _user.emailsec: update_user(_email, UserConfig.NAME, _req_dict["emailsec"])

    elif request.method == Method.DELETE:
        return


@app.route("/note", methods=[Method.POST, Method.PUT, Method.DELETE])
def note():
    if request.method == Method.POST:
        return

    elif request.method == Method.PUT:
        return

    elif request.method == Method.DELETE:
        return


if __name__ == '__main__':
    app.run(debug=True)
