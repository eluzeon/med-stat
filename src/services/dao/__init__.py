import functools
import typing

from src import store


def memoize(key: str) -> typing.Callable[[typing.Any], typing.Any]:
    """
    Запоминает возвращаемое значение функции в первый раз
    и возвращает его в последующие разы без перерасчета
    """
    def _actual_decorator(fn: typing.Callable[[typing.Any], typing.Any]):
        @functools.wraps(fn)
        def _wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            if val := store.get(key):
                # if value persists -> return it
                return val
            out = fn(*args, **kwargs)
            store.push(key, out)
            return out
        return _wrapper
    return _actual_decorator
