from sqlalchemy import create_engine
from json import load

try:
    with open('db/config.json', 'r') as file:
        acess = load(file)
except:
    open('config.json', "x")

conn = f"mysql+pymysql://{acess['user']}:{acess['password']}@{acess['host']}" \
       f"/{acess['database']}?charset={acess['charset']}"
engine = create_engine(conn, echo=True, future=True)
engine.echo = False
