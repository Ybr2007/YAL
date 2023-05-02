import typing
import warnings

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QResizeEvent, QIcon
from PyQt5.QtCore import pyqtSignal, QSize, QPoint, QObject, QEvent


class ListWidget(QWidget):
    """
    纵向列表控件
    注: 该控件直接派生自QWidget而不是QListWidget
    该控件可以自动适应列表中控件的尺寸而设置自身高度
    """
    heightChangeSignal = pyqtSignal(int, int)  # int: 当前高度, int: 高度变化量

    def __init__(self):
        super().__init__()

        self.items: list[QWidget] = []  # 所有控件
        self._height = 0  # 高度
        self.spacing = 0  # 控件间距

    def setSpacing(self, spacing: int):
        """设置控件间距

        Args:
            spacing (int): 间距
        """
        deltaHeight = 0
        for item in self.items:
            item.move(0, item.y() + deltaHeight)
            deltaHeight += (spacing - self.spacing)

        self.updateHeight(deltaHeight - (spacing - self.spacing))  # 去掉最后一个控件后多余的间隔
        self.spacing = spacing

    def _registerItem(self, item: QWidget, index: typing.Optional[int]=None):
        """注册控件

        Args:
            item (QWidget): 控件
            index (typing.Optional[int], optional): 控件插入位置序号, 默认添加到末尾
        """
        item.setParent(self)
        item.show()
        item.installEventFilter(self)  # 为控件安装事件过滤器以捕获控件的QResizeEvent
        if index is None:
            self.items.append(item)  # 加入到控件列表末尾
        else:
            self.items.insert(index, item)  # 插入到控件列表

    def itemCount(self) -> int:
        """获取列表中控件数量

        Returns:
            int: 列表中控件数量
        """
        return len(self.items)

    def appendItem(self, item: QWidget):
        """添加控件（到末尾）

        Args:
            item (QWidget): 控件
        """
        self.insertItem(item, self.itemCount())

    def insertItem(self, item: QWidget, index: int):
        """插入控件到指定位置

        Args:
            item (QWidget): 控件
            index (int): 位置序号
        """
        self._registerItem(item, index)

        item.setFixedWidth(self.width())
        
        height = 0
        for i in range(index):
            height += self.items[i].height() + self.spacing
        
        if self.itemCount() == 1:  # 如果是列表里唯一一个控件，则不考虑间距
            item.move(0, height - item.height())
            self.updateHeight(item.height(), index - 1)
        else:
            item.move(0, height - item.height() - self.spacing)
            self.updateHeight(item.height() + self.spacing, index - 1)

    def removeItem(self, item: QWidget):
        """删除控件

        Args:
            item (QWidget): 控件
        Warnings:
            参数"item"错误：控件不在该列表中
        """
        if item in self.items:
            itemIndex = self.items.index(item)
            self.removeItemAt(itemIndex)
        else:
            warnings.warn('参数"item"错误：控件不在该列表中')
       
    def removeItemAt(self, index: int):
        """删除指定位置的控件

        Args:
            index (int): 控件位置序号
        """
        item = self.items[index]
        item.setParent(None)  # type: ignore
        deltaHeight = - item.height() - self.spacing

        self.updateHeight(deltaHeight, index)
        del self.items[index]

    def updateHeight(self, deltaHeight: int, updateItemBelowIndex: typing.Optional[int]=None):
        """更新高度

        Args:
            deltaHeight (int): 高度变化量
            updateItemBelowIndex (typing.Optional[int], optional): 更新该参数对应控件以下控件（不包含该控件）的位置, 
            默认不更新任何控件
        """
        self._height += deltaHeight
        self._height = max(self._height, 0)
        self.setFixedHeight(self._height)
        self.heightChangeSignal.emit(self._height, deltaHeight)

        if updateItemBelowIndex is not None:
            for i in range(updateItemBelowIndex + 1, len(self.items)):
                item = self.items[i]
                item.move(item.pos() + QPoint(0, deltaHeight))

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """事件过滤器(重新Qt方法)"""
        if isinstance(event, QResizeEvent) and isinstance(obj, QWidget) and obj in self.items:
            if event.oldSize() != QSize(-1, -1):  # 忽略创建时的resize事件
                deltaHeight = event.size().height() - event.oldSize().height()
                itemIndex = self.items.index(obj)
                self.updateHeight(deltaHeight, itemIndex)

        return super().eventFilter(obj, event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """重写Qt方法, 同步控件与列表宽度"""
        for item in self.items:
            item.setFixedWidth(event.size().width())
        return super().resizeEvent(event)


class ListWidgetWithBtn(ListWidget):
    """
    带有添加和删除按钮的ListWidget
    """
    def __init__(self):
        super().__init__()

        self.addItemBtnHeight = 30  # 添加按钮高度
        self.removeItemBtns: list[typing.Optional[QPushButton]] = []  # 删除按钮列表
        self.removeItenBtnSpacing = 4  # 删除按钮（与列表中控件）的间距
        self.removeItemBtnSize = QSize(30, 30)  # 删除按钮尺寸
        self.itemCountRange: list[int] = []  # 允许添加/删除到的控件数量最大值/最小值

        self.addItemButton = QPushButton()  # 添加按钮
        self.addItemButton.setFixedHeight(self.addItemBtnHeight)
        self.addItemButton.pressed.connect(self.onAddItemBtnPress)
        self.appendItem(self.addItemButton)

    def insertItem(self, item: QWidget, index: int):
        super().insertItem(item, index)

        item.setFixedWidth(self.width() - self.removeItemBtnSize.width() - self.removeItenBtnSpacing)  # 留出删除按钮间隔的位置

        if item is not self.addItemButton:
            removeItemBtn = QPushButton(self)
            self.removeItemBtns.insert(index, removeItemBtn)
            removeItemBtn.setIcon(QIcon(":/Img/Remove.png"))
            removeItemBtn.move(
                self.width() - self.removeItemBtnSize.width(), 
                item.y() + item.height()//2 - self.removeItemBtnSize.height()//2  # 删除按钮居中
            )
            removeItemBtn.setFixedSize(self.removeItemBtnSize)
            removeItemBtn.pressed.connect(lambda: self.removeItem(item))
            removeItemBtn.show()
        else:
            self.removeItemBtns.insert(index, None)  # 不为添加按钮设置删除按钮

        self.checkItemCount()  # 检查控件数量

    def resizeEvent(self, event: QResizeEvent) -> None:
        for item in self.items:
            if not item is self.addItemButton: 
                # 在删除按钮被禁用的情况下不留出按钮间隔的位置
                if self.itemCountRange and self.itemCount() - 1 <= self.itemCountRange[0]:
                    item.setFixedWidth(event.size().width())
                else:
                    item.setFixedWidth(
                        event.size().width() - self.removeItemBtnSize.width() - self.removeItenBtnSpacing
                    )  # 留出删除按钮间隔的位置
        self.addItemButton.setFixedWidth(event.size().width())

    def removeItemAt(self, itemIndex: int):
        if itemIndex == self.itemCount() - 1:
            raise ValueError("addItemButton不能被删除")
        
        super().removeItemAt(itemIndex)
        self.removeItemBtns[itemIndex].deleteLater()  # type: ignore
        del self.removeItemBtns[itemIndex]

        self.checkItemCount()  # 检查控件数量

    def updateHeight(self, deltaHeight: int, updateItemBelowIndex: typing.Optional[int]=None):
        """更新高度

        Args:
            deltaHeight (int): 高度变化量
            updateItemBelowIndex (typing.Optional[int], optional): 更新该参数对应控件以下控件（不包含该控件）的位置, 
            默认不更新任何控件
        """
        super().updateHeight(deltaHeight, updateItemBelowIndex)

        if updateItemBelowIndex is not None and updateItemBelowIndex >= 0:
            for i in range(updateItemBelowIndex, len(self.removeItemBtns)):
                item = self.items[i]
                removeItemBtn = self.removeItemBtns[i]
                if removeItemBtn is not None:
                    removeItemBtn.move(
                        self.width() - self.removeItemBtnSize.width(), 
                        item.y() + item.height()//2 - self.removeItemBtnSize.height() // 2  # 删除按钮居中
                    )

    def checkItemCount(self):
        """检查控件数量"""
        if self.itemCountRange:
            if self.itemCount() - 1 >= self.itemCountRange[1]:
                self.addItemButton.setVisible(False)
            else:
                self.addItemButton.setVisible(True)

            if self.itemCount() - 1 <= self.itemCountRange[0]:
                for removeItemBtn in self.removeItemBtns:
                    if removeItemBtn is not None:
                        removeItemBtn.setVisible(False)
            else:
                for removeItemBtn in self.removeItemBtns:
                    if removeItemBtn is not None:
                        removeItemBtn.setVisible(True)
        self.resizeEvent(QResizeEvent(self.size(), self.size()))

    def onAddItemBtnPress(self):
        """添加按钮点击回调"""
        ...
        
    def addItem(self, item: QWidget):
        """
        向列表中添加新控件（添加按钮之前）
        
        Returns:
            QWidget: 新控件
        """
        self.insertItem(item, len(self.items) - 1)
