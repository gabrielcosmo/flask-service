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
            _email = _req.get('email')
            _pw = _req.get('password')

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
            _req = request.get_json()
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


@app.route("/note", methods=[Method.POST, Method.PUT, Method.DELETE, Method.GET])
def note():
    global validate
    validate = True

    if request.method == Method.GET:
        try:
            user_id = request.args["userId"]
            id = request.args["id"]
            _note = select_note(id)

        except:
            return make_response(jsonify({"messege": f"Invalid values"}))

        else:
            if _note.user_id == int(user_id):
                return make_response(jsonify({
                    "id": _note.id,
                    "title": _note.title,
                    "text": _note.text,
                    "record": _note.record,
                    "modified": _note.modified,
                    "favorite": _note.favorite,
                    "tags": _note.tags
                })
                )
            else:
                return make_response(jsonify({"messege": f"invalid user id for note {_note.title}"}))

    elif request.method == Method.POST:

        try:
            _req = request.get_json()
            user_id = _req.get("userId")
            _id = _req.get("id")
            _title = _req.get("title")
            _text = _req.get("text")

        except:
            return make_response(jsonify({"messege": f"Invalid values"}))

        else:
            _note = select_note(_id)
            if _note is None:
                insert_note(_title, _text, user_id)
                _n = select_note(_id)

                return make_response(jsonify({
                    "id": _n.id,
                    "title": _n.title,
                    "text": _n.text,
                    "record": _n.record,
                    "modified": _n.modified,
                    "favorite": _n.favorite,
                    "tags": _n.tags
                }))
            else:
                return make_response(jsonify({"messege": f"Id invalid"}))

    elif request.method == Method.PUT:

        try:
            _req = request.get_json()
            _id = _req.get("id")
            obj_data = _req.get("userData")

            _fields = []

        except Exception as err:
            return make_response(jsonify({
                "messege": "Invalid fields or not send expected fields", "erro": f"{err}"
            }))

        else:
            for k in obj_data.keys():
                _fields.append(k)

            _note = select_note(_id)
            if _note is not None:
                if NoteConfig.TITLE.value in obj_data.keys():
                    if obj_data[NoteConfig.TITLE.value] != _note.title:
                        update_note(_id, NoteConfig.TITLE, obj_data["title"])

                elif NoteConfig.TEXT.value in obj_data.keys():
                    if obj_data[NoteConfig.TEXT.value] != _note.text:
                        update_note(_id, NoteConfig.TEXT, obj_data["text"])

                elif NoteConfig.FAVORITE.value in obj_data.keys():
                    valid = [0, 1]
                    if obj_data[NoteConfig.FAVORITE.value] != _note.favorite and obj_data.get("favorite") in valid:
                        update_note(_id, NoteConfig.FAVORITE, obj_data["favorite"])

                elif NoteConfig.TAGS.value in obj_data.keys():
                    if obj_data[NoteConfig.TAGS.value] != _note.tags:
                        update_note(_id, NoteConfig.TAGS, obj_data["tags"])

                else:
                    validate = False

        finally:
            if validate:
                return make_response(jsonify({"messege": "sucess"}))
            else:
                return make_response(jsonify({"messege": "found fields out context"}))

    elif request.method == Method.DELETE:

        try:
            _req = request.get_json()
            _note_id = _req.get("id")
            _email = _req.get("email")
            _pw = _req.get("password")

            _user = select_user(_email)
            _note = select_note(_note_id)

        except:
            return make_response(jsonify({
                "messege": "Expected fields or invalid values"
            }))

        else:
            if (_user is not None) and (_note is not None):
                if _user.password == _pw:
                    if _note.user_id == _user.id:
                        delete_note(_note_id)
                        return make_response(jsonify({
                            "messege": "Sucess"
                        }))
                    else:
                        return make_response(jsonify({
                            "messege": f"This user not is owner of note with id {_note_id}"
                        }))
                else:
                    return make_response(jsonify({
                        "messege": "User not identified"
                    }))
            else:
                return make_response(jsonify({
                    "messege": "User or Note  not identified"
                }))


if __name__ == '__main__':
    app.run(debug=True)
