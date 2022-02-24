import typing

_store = {}


def clear():
    _store.clear()


def push(key: str, value: typing.Any) -> typing.Any:
    _store[key] = value


def get(key: str) -> typing.Any:
    return _store.get(key)
