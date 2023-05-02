import typing

from PyQt5.QtCore import QTimer


class TimeLine:
    def __init__(self):
        self._actions: list[tuple[float, typing.Callable, tuple]] = []
        self._timers: list[QTimer] = []

    def addAction(self, secTime: float, action: typing.Callable, args: typing.Optional[tuple]=None) -> "TimeLine":
        if not args:
            args = ()
        self._actions.append((secTime, action, args))

        return self

    def run(self) -> "TimeLine":
        maxTime = -1
        maxTimeIndex = None

        for i, (secTime, action, args) in enumerate(self._actions):
            if secTime <= 0:
                action(*args)
            else:
                timer = QTimer()
                timer.timeout.connect(lambda: action(*args))
                timer.timeout.connect(timer.stop)
                timer.start(secTime * 1000)

                if secTime > maxTime:
                    maxTime = secTime
                    maxTimeIndex = len(self._timers)

                self._timers.append(timer)

        if maxTimeIndex:
            self._timers[maxTimeIndex].timeout.connect(self._timers.clear)

        self._actions.clear()

        return self
