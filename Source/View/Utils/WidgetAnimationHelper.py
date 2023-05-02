import typing

from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import QObject, QPoint, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import pyqtProperty  # type: ignore


class WidgetAnimationHelper(QObject):
    def __init__(self, widget: typing.Optional[QWidget]=None) -> None:
        super().__init__(widget)

        self._widget = widget

        self._animations: dict[str, QPropertyAnimation] = {}
        self._opacityEffect = QGraphicsOpacityEffect(self)

        if self._widget is not None:
            self._widget.setGraphicsEffect(self._opacityEffect)

    def setWidget(self, widget: typing.Optional[QWidget]=None):
        self._widget = widget

        if self._widget is not None:
            self._widget.setGraphicsEffect(self._opacityEffect)

    """
    Properties
    """
    ## Property: fixedSize
    # get

    def __getFixedSizeP(self) -> QSize:
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        return self._widget.size()

    # set
    def __setFixedSizeP(self, size: QSize) -> None:
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        self._widget.setFixedSize(size)

    # define
    fixedSize = pyqtProperty(QSize, __getFixedSizeP, __setFixedSizeP)

    ## Property: width
    # get

    def __getWidthP(self) -> int:
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        return self._widget.width()

    # set
    def __setWidthP(self, width: int) -> None:
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        self._widget.setFixedWidth(width)

    # define
    width = pyqtProperty(int, __getWidthP, __setWidthP)

    # Property: height
    # get

    def __getHeightP(self) -> int:
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        return self._widget.height()

    # set
    def __setHeightP(self, height: int) -> None:
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        self._widget.setFixedHeight(height)

    # define
    height = pyqtProperty(int, __getHeightP, __setHeightP)

    # Property: opacity
    # get

    def __getOpacityP(self) -> int:
        return int(self._opacityEffect.opacity() * 255)

    # set
    def __setOpacityP(self, opacity: int) -> None:
        self._opacityEffect.setOpacity(opacity / 255)

    # define
    opacity = pyqtProperty(int, __getOpacityP, __setOpacityP)

    """
    Property Setters
    """

    def setPos(self, pos: QPoint, durationSecond: float = 0,
                easingCurve: QEasingCurve.Type = QEasingCurve.Type.InOutQuint,
                finishCallback: typing.Optional[typing.Callable]=None) -> "WidgetAnimationHelper":
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        
        if durationSecond <= 0:
            self._widget.move(pos)
        else:
            if "pos" in self._animations:
                self._animations["pos"].stop()

            anim = QPropertyAnimation(self._widget, b"pos", self)
            anim.setStartValue(self._widget.pos())
            anim.setEndValue(pos)
            anim.setDuration(int(durationSecond * 1000))
            if easingCurve:
                anim.setEasingCurve(easingCurve)
            if finishCallback:
                anim.finished.connect(finishCallback)
            anim.start()
            self._animations["pos"] = anim

        return self    

    def setSize(self, size: QSize, durationSecond: float = 0,
                 easingCurve: QEasingCurve.Type = QEasingCurve.Type.InOutQuint,
                 finishCallback: typing.Optional[typing.Callable]=None) -> "WidgetAnimationHelper":
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        
        if durationSecond <= 0:
            self._widget.resize(size)
        else:
            if "size" in self._animations:
                self._animations["size"].stop()

            anim = QPropertyAnimation(self._widget, b"size", self)
            anim.setStartValue(self._widget.size())
            anim.setEndValue(size)
            anim.setDuration(int(durationSecond * 1000))
            if easingCurve:
                anim.setEasingCurve(easingCurve)
            if finishCallback:
                anim.finished.connect(finishCallback)
            anim.start()
            self._animations["size"] = anim

        return self

    def setFixedSize(self, size: QSize, durationSecond: float = 0,
                 easingCurve: QEasingCurve.Type = QEasingCurve.Type.InOutQuint,
                 finishCallback: typing.Optional[typing.Callable]=None) -> "WidgetAnimationHelper":
        if self._widget is None:
            raise RuntimeError("Target widget is None")
        
        if durationSecond <= 0:
            self.__setFixedSizeP(size)
        else:
            if "fixedSize" in self._animations:
                self._animations["fixedSize"].stop()

            anim = QPropertyAnimation(self, b"fixedSize", self)
            anim.setStartValue(self.__getFixedSizeP())
            anim.setEndValue(size)
            anim.setDuration(int(durationSecond * 1000))
            if easingCurve:
                anim.setEasingCurve(easingCurve)
            if finishCallback:
                anim.finished.connect(finishCallback)
            anim.start()
            self._animations["fixedSize"] = anim

        return self

    def setWidth(self, width: int, durationSecond: float = 0,
                  easingCurve: QEasingCurve.Type = QEasingCurve.Type.InOutQuint,
                  finishCallback: typing.Optional[typing.Callable]=None) -> "WidgetAnimationHelper":
        if self._widget is None:
            raise RuntimeError("Target widget is None")

        if durationSecond <= 0:
            self.__setWidthP(width)
        else:
            if "width" in self._animations:
                self._animations["width"].stop()

            anim = QPropertyAnimation(self, b"width", self)
            anim.setStartValue(self.__getWidthP())
            anim.setEndValue(width)
            anim.setDuration(int(durationSecond * 1000))
            if easingCurve:
                anim.setEasingCurve(easingCurve)
            if finishCallback:
                anim.finished.connect(finishCallback)
            anim.start()
            self._animations["width"] = anim

        return self

    def setHeight(self, height: int, durationSecond: float = 0,
                   easingCurve: QEasingCurve.Type = QEasingCurve.Type.InOutQuint,
                   finishCallback: typing.Optional[typing.Callable]=None) -> "WidgetAnimationHelper":
        if self._widget is None:
            raise RuntimeError("Target widget is None")

        if durationSecond <= 0:
            self.__setHeightP(height)
        else:
            if "height" in self._animations:
                self._animations["height"].stop()

            anim = QPropertyAnimation(self, b"height", self)
            anim.setStartValue(self.__getHeightP())
            anim.setEndValue(height)
            anim.setDuration(int(durationSecond * 1000))
            if easingCurve:
                anim.setEasingCurve(easingCurve)
            if finishCallback:
                anim.finished.connect(finishCallback)
            anim.start()
            self._animations["height"] = anim

        return self
    
    def setOpacity(self, opacity: int, durationSecond: float = 0,
                   easingCurve: QEasingCurve.Type = QEasingCurve.Type.InOutQuint,
                   finishCallback: typing.Optional[typing.Callable]=None) -> "WidgetAnimationHelper":
        if self._widget is None:
            raise RuntimeError("Target widget is None")

        if durationSecond <= 0:
            self.__setOpacityP(opacity)
        else:
            if "opacity" in self._animations:
                self._animations["opacity"].stop()

            anim = QPropertyAnimation(self, b"opacity", self)
            anim.setStartValue(self.__getOpacityP())
            anim.setEndValue(opacity)
            anim.setDuration(int(durationSecond * 1000))
            if easingCurve:
                anim.setEasingCurve(easingCurve)
            if finishCallback:
                anim.finished.connect(finishCallback)
            anim.start()
            self._animations["opacity"] = anim

        return self