import typing


T = typing.TypeVar('T')

def Try(obj: typing.Optional[T]) -> T:
    """将一个可选类型的obj断言为非None类型，如果obj为None则报出运行时错误

    Args:
        obj (typing.Optional[T]): 对象

    Raises:
        TypeError: obj为None

    Returns:
        T: 对象
    """
    if obj is None:
        raise TypeError("obj is None")
    return obj