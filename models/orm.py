from sqlalchemy import insert, select
from engine import engine, session_factory
from models import User

def insert_data():
    with session_factory() as session:
        user_oleg = User(username="oleg") 
        user_vova = User(username="vova") 
        session.add_all([user_oleg,user_vova])
        session.commit()

def select_data():
    with engine.connect() as eng:
        query = select(User)
        result = eng.execute(query)
        workers = result.all()
        print(workers)
select_data()
