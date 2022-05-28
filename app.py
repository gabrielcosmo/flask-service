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


@app.route("/user", methods=[Method.POST, Method.PUT, Method.DELETE, Method.GET])
def user():
    global validate  # variaável de validação para requisições PUT
    validate = False  # inicia-se como False

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

                # obrigatoriamente, deve-se informar um nome para o usuário, caso não é lançada uma exceção
                except:
                    return jsonify({"messege": "'name' not found during user criation"})

    elif request.method == Method.PUT:
        try:
            _req = request.args
            _email = _req.get("email")
            _pw = _req.get("password")
            _user = select_user(_email)

        except:
            return make_response(jsonify({"messege": "fail"}))

        else:
            if _user.password == _pw:
                user_data = (_req.get("user")).copy()
                fields = []
                validate = True  # os dados são válidos até que se comprove o contrário

                for k in user_data.keys():  # os campos do corpo da requisição são registrados em 'fields'
                    fields.append(k)

                # region ANALISE DOS DADOS
                """
                + A primeira condicional testa se um dado campo foi informado no corpo da requisição (ex.: noma, email, etc.);
                + A segunda se o valor desse campo informado difere do valor do campo correspondente na instância;
                + Se nenhum campo que pertence a instãncia foi declarado no na requisição 'validate' é falso.
                """
                if UserConfig.NAME.value in fields:
                    if user_data[UserConfig.NAME.value] != _user.name:
                        update_user(_email, UserConfig.NAME, user_data["name"])

                elif UserConfig.EMAIL.value in fields:
                    if user_data[UserConfig.EMAIL.value] != _user.email:
                        update_user(_email, UserConfig.EMAIL, user_data["email"])

                elif UserConfig.PASSWORD.value in fields:
                    if user_data[UserConfig.PASSWORD.value] != _user.password:
                        update_user(_email, UserConfig.PASSWORD, user_data["password"])

                elif UserConfig.EMAILSEC.value in fields:
                    if user_data[UserConfig.EMAILSEC.value] != _user.emailsec:
                        update_user(_email, UserConfig.EMAILSEC, user_data["emailsec"])
                else:
                    validate = False
                # endregion
        finally:
            if validate:
                return make_response(jsonify({"messege": "sucess"}))
            else:
                return make_response(jsonify({"messege": "found fields out context"}))

    elif request.method == Method.DELETE:
        try:
            _req = request.get_json()
            _email = _req["email"]
            _pw = _req["password"]
            _user = select_user(_email)

        except:
            return make_response(jsonify({"messege": "fail"}))

        else:
            if _user is None:
                return make_response(jsonify({"messege": "user not found"}))

            elif _user.password == _pw:
                delete_user(_email)
                return make_response(jsonify({"messege": "sucess"}))

            else:
                return make_response(jsonify({"messege": f"invalid password for user {_user.name}"}))


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
