# 定义一个信号发射器类
from PyQt5.QtCore import QObject, pyqtSignal


class SignalEmitter(QObject):
    # 这里可以定义多个信号用于不同的回调函数
    file_processed = pyqtSignal(str)  # 定义一个信号，携带文件路径信息
