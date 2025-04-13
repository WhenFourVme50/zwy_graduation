from db import session

from crud import user_crud

db_session = session.get_session()

test_phone = "10***024"
print(dict(user_crud.get_user_by_phone(db_session,test_phone)))