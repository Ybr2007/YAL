import typing


def singleton(cls: type) -> typing.Callable:
    """
    将一个类型变为单例模式
    """
    _instance = {}

    def inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    
    return inner