from functools import wraps


def handle_assertion_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            message = await func(*args, **kwargs)

            return message
        except AssertionError as e:
            return {'message': str(e)}

    return wrapper
