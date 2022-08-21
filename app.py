from flask import Flask, request, make_response, jsonify
import json
import datetime
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
    if request.method == Method.GET:
        try:
            email = request.args["email"]
            _user = select_user(email)
        except:
            _users: list = select_all_users()
            response = []
            for _user in _users:
                response.append({
                    "id": _user.id,
                    "name": _user.name,
                    "email": _user.email,
                    "password": _user.password,
                    "emailsec": _user.emailsec,
                    "record": _user.record
                })
            return make_response(jsonify(response))
        else:
            return make_response(jsonify({
                "id": _user.id,
                "name": _user.name,
                "email": _user.email,
                "password": _user.password,
                "emailsec": _user.emailsec,
                "record": _user.record
            }))

    if request.method == Method.POST:
        try:
            _req = request.get_json()
            _email = _req.get('email')
            _pw = _req.get('password')
        except:
            return make_response(jsonify({"messege": "fail"}))
        else:
            try:
                _user = select_user(_email)
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
            except:
                try:
                    insert_user(request.args["name"], _email, _pw)
                except:
                    return jsonify({"messege": "'name' not found during user criation"})

    elif request.method == Method.PUT:
        try:
            validate = True
            _data = request.data.decode()
            _req: dict = json.loads(_data)
            _email = _req["email"]
            _user = select_user(_email)

        except:
            return make_response(jsonify({"messege": "Email not found"}))

        try:
            if _user is not None:
                update_user(_email, UserConfig.NAME, _req["name"])
                update_user(_email, UserConfig.EMAIL, _req["email"])
                update_user(_email, UserConfig.EMAILSEC, _req["emailsec"])
                update_user(_email, UserConfig.PASSWORD, _req["password"])
            else:
                validate = False
                return make_response(jsonify({"messege": "Email not found"}))
        except:
            validate = False
            return make_response(jsonify({"messege": "Request format invalid!"}))

        finally:
            if validate: return make_response(jsonify({"messege": "sucess"}))

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
    if request.method == Method.GET:
        try:
            id = request.args["id"]
            _note = select_note(id)

        except:
            notes: list = select_all_notes()
            response = []
            for _note in notes:
                response.append({
                    "id": _note.id,
                    "title": _note.title,
                    "text": _note.text,
                    "record": _note.record,
                    "modified": _note.modified,
                    "favorite": _note.favorite,
                    "tags": _note.tags
                })
            return make_response(jsonify(response))

        else:
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
            validate = True
            _data = request.data.decode()
            _req: dict = json.loads(_data)
            _id = _req["id"]
            _note = select_note(_id)

        except:
            return make_response(jsonify({"messege": "Id not found"}))

        try:
            if _note is not None:
                update_note(_id, NoteConfig.TITLE, _req["title"])
                update_note(_id, NoteConfig.TEXT, _req["text"])
                update_note(_id, NoteConfig.FAVORITE, _req["favorite"])
                update_note(_id, NoteConfig.TAGS, _req["tags"])
                update_note(_id, NoteConfig.MODIFIED, datetime.now())
            else:
                validate = False
                return make_response(jsonify({"messege": "Id not found"}))
        except:
            validate = False
            return make_response(jsonify({"messege": "Request format invalid!"}))

        finally:
            if validate: return make_response(jsonify({"messege": "sucess"}))

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
