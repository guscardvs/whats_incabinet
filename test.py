from typing import Generic, TypeVar, get_type_hints, get_args
from inspect import signature

T = TypeVar("T")


class Test(Generic[T]):
    def __init__(self, val: T) -> None:
        self.val = val

    def my_type(self) -> type[T]:
        return type(self.val)


def get_val(val: Test[int], oth_val):
    return val.val + oth_val


test = Test(1)

print("val" in signature(get_val).parameters)
