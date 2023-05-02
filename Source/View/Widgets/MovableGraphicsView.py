from PyQt5.QtWidgets import QGraphicsView, QFrame, QApplication
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QPoint


class MovableGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        # 缩放相关参数
        self.zoomInFactor = 1.25
        self.zoom = 5
        self.zoomStep = 1
        self.zoomLimit = False
        self.zoomRange = [0, 10]

        # 视野拖拽数据
        self.inViewMovementMode = False
        self.viewMovementStartPos = QPoint()
        self.centerPos = QPoint()

        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.initUI()

    def initUI(self):
        """
        初始化界面设置
        """
        # 设置抗锯齿和平滑缩放
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | 
                            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        # 防止拖拽产生残影
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setFrameShape(QFrame.Shape.NoFrame)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        鼠标按下事件(重写qt方法)
        """
        
        shouldMove = event.button() == Qt.MouseButton.LeftButton and \
            QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier

        # 开始拖拽视野
        if shouldMove:
            self.inViewMovementMode = True
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            super().mousePressEvent(event)

        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        鼠标松开事件(重写qt方法)
        """
        super().mouseReleaseEvent(event)

        # 结束拖拽视野
        if self.inViewMovementMode:
            self.inViewMovementMode = False
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def wheelEvent(self, event):
        """
        滚轮滚动事件(重写qt方法)
        """
        #计算缩放系数
        zoomOutFactor = 1 / self.zoomInFactor

        #计算缩放
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        #设置场景比例
        if not clamped or self.zoomLimit:
            self.scale(zoomFactor, zoomFactor)