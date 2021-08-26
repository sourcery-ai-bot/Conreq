from functools import wraps
from typing import Callable

from conreq import app


def user_setting() -> Callable:
    """Decorates an IDOM component. Component is injected into the user settings modal.
    Settings component will be provided the websocket scope.
    """

    def decorator(func):

        app.config("user_setting_components").append(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator
