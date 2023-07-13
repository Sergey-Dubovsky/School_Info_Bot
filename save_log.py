from ast import Pass
from with_session import with_session
from models.log import Log

@with_session
def save_log(session,info,user_id,user_firstname,user_lastname,user_username):
    session.add(  # добавление записи в лог
        Log(
            info = info,
            user_id = user_id,
            user_username = user_username,
            user_firstname = user_firstname,
            user_lastname = user_lastname,
            )
    )
    session.commit()
