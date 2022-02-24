import typing
from itertools import zip_longest

T = typing.TypeVar("T")


def pairs(it: typing.Iterable[T]) -> typing.Iterable[tuple[T, T]]:
    """
    Given list of T, returns list of "paired" objects.
    For example
    >>> pairs([1,2,3,4,5])
    <<< ((1,2), (3,4), (5, None))
    """
    return zip_longest(
        it[::2], it[1::2]
    )


def first(itr: typing.Iterable[T]) -> typing.Optional[T]:
    return next(iter(itr), None)


def last(itr: typing.Sequence[T]) -> typing.Optional[T]:
    return first(reversed(itr))


def find(fn: typing.Callable[[T], bool], itr: typing.Iterable[T]) -> typing.Optional[T]:
    return next(filter(fn, itr), None)
