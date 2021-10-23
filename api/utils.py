from functools import wraps


def handle_value_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            message = await func(*args, **kwargs)

            return message
        except ValueError as e:
            return {'message': str(e)}

    return wrapper
