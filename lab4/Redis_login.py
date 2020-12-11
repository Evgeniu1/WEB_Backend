from flask import session
from redis import Redis
redis = Redis(host='127.0.0.1', port=6379)

USER = "admin"
PASS = "admin"

def login_decorator(func):
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return 'error', 403
        redis_user_id = redis.get(user_id).decode()
        if redis_user_id != '1':
            return 'error', 403
        return func(*args, **kwargs)
    return wrapper


def login_user(user_id):
    session['user_id'] = user_id
    redis.set(user_id, '1', 60*60*10)


def logout_user():
    session.pop('user_id')
    redis.delete('user_id') 
