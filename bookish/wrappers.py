from functools import wraps

from pip._internal.network import session

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        if 'api_session_token' not in session:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return {"message" : "Access denied"}

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_token