from factory import engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from models.models import NoteModel, UserModel, UserConfig, NoteConfig
from datetime import datetime


#region User
def insert_user(name, email, password, emailsec=""):
    session = Session(engine)

    user = UserModel(name=name, email=email, password=password, record=datetime.today(), emailsec=emailsec)

    session.add(user)

    session.commit()
    session.close()


def update_user(email, field: UserConfig, value):
    session = Session(engine)

    sql = f"UPDATE `user` SET `{field.name}` = {value} WHERE `email`='{email}'"
    session.execute(text(sql))

    session.commit()
    session.close()


def select_user(user_email):
    session = Session(engine)
    select = session.query(UserModel).where(UserModel.email == user_email)

    session.close()

    return select.first()


def select_all_users():
    session = Session(engine)
    select = session.query(UserModel).all()
    session.close()

    return select


def delete_user(email):
    session = Session(engine)

    user = session.query(UserModel).where(UserModel.email == email)
    session.delete(user.first())

    session.commit()
    session.close()


#endregion

#region Note
def insert_note(title, text, user_id):
    session = Session(engine)
    record = datetime.today()
    note = NoteModel(title=title, text=text, user_id=user_id, record=record, modified=record, favorite=False)

    session.add(note)

    session.commit()
    session.close()


def update_note(title, field: NoteConfig, value):
    session = Session(engine)

    sql = f"UPDATE `note` SET `{field.name}` = '{value}' WHERE `title`='{title}'"
    session.execute(text(sql))

    session.commit()
    session.close()


def select_note(note_title):
    session = Session(engine)
    select = session.query(NoteModel).where(NoteModel.title == note_title)

    session.close()

    return select.first()


def select_all_notes():
    session = Session(engine)
    select = session.query(NoteModel).all()
    session.close()

    return select


def delete_note(title):
    session = Session(engine)

    note = session.query(NoteModel).where(NoteModel.title == title)
    session.delete(note.first())

    session.commit()
    session.close()
#endregion
