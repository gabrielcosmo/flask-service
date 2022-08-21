import requests
import json

# region /USER TEST
def user_get():
    req = requests.get("http://127.0.0.1:5000/user")
    return {
        "code": req.status_code,
        "json": req.json(),
    }

def user_post(**body):
    req = requests.post("http://127.0.0.1:5000/user", json.dumps(body))

    return {
        "code": req.status_code,
        "json": req.json(),
    }


def user_put(**body):
    req = requests.put("http://127.0.0.1:5000/user", json.dumps(body))

    return {
        "code": req.status_code,
        "json": req.json(),
    }


def user_delete(**body):
    req = requests.post("http://127.0.0.1:5000/user", json.dumps(body))

    return {
        "code": req.status_code,
        "json": req.json(),
    }


# endregion

# region /NOTE TESTS
def note_get(id):
    req = requests.get(f"http://127.0.0.1:5000/note?id={id}")
    return {
        "code": req.status_code,
        "json": req.json(),
    }


def note_post(**body):
    req = requests.post("http://127.0.0.1:5000/note", json.dumps(body))

    return {
        "code": req.status_code,
        "json": req.json(),
    }


def note_put(**body):
    req = requests.put("http://127.0.0.1:5000/note", json.dumps(body))

    return {
        "code": req.status_code,
        "json": req.json(),
    }


def note_delete(**body):
    req = requests.post("http://127.0.0.1:5000/note", json.dumps(body))

    return {
        "code": req.status_code,
        "json": req.json(),
    }
# endregion
