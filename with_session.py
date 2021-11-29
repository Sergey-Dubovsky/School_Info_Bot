from functools import wraps
from models.database import Session


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = Session()
        result = func(session, *args, **kwargs)
        session.close()
        return result

    return wrapper
