
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMenu, QAction, QSystemTrayIcon, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QIcon, QMovie
import os

from signal import SignalEmitter

from threading import Thread



class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_thread = None
        self.movie = None
        self.offset = None
        self.is_dragging = None
        self.label = None
        self.tray_icon = None  # 托盘图标对象
        # 创建信号发射器
        self.file_signal_emitter = SignalEmitter()
        self.file_signal_emitter.file_processed.connect(self.on_file_processed)  # 连接信号到槽函数
        self.initUI()

    def initUI(self):
        self.setWindowTitle('桌宠')

        # 设置窗口透明背景
        self.setWindowFlag(Qt.FramelessWindowHint)  # 去掉边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 窗口置顶
        self.setGeometry(500, 500, 150, 150)

        # 创建 QLabel 显示动图
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 150, 150)
        self.change_state('idle')

        # 初始化拖动相关变量
        self.is_dragging = False
        self.offset = QPoint(0, 0)

        # 设置右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 添加托盘图标
        self.init_tray_icon()

        # 启用拖拽功能
        self.setAcceptDrops(True)

    def init_tray_icon(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)

        # 设置托盘图标的图标（替换为您的图标路径）
        self.tray_icon.setIcon(QIcon("assets/icon.ico"))

        # 创建托盘右键菜单
        tray_menu = QMenu(self)

        # 添加菜单项
        show_action = QAction(QIcon("assets/show.ico"), "显示桌宠", self)
        show_action.triggered.connect(self.show_window)

        hide_action = QAction(QIcon("assets/hide.ico"), "隐藏桌宠", self)
        hide_action.triggered.connect(self.hide)

        quit_action = QAction(QIcon("assets/exit.ico"), "退出", self)
        quit_action.triggered.connect(self.quit_application)

        # 添加菜单项到托盘菜单
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        # 将菜单绑定到托盘图标
        self.tray_icon.setContextMenu(tray_menu)

        # 显示托盘图标
        self.tray_icon.show()

    def show_window(self):
        # 显示窗口并激活
        self.showNormal()
        self.activateWindow()

    def quit_application(self):
        # 退出应用程序
        QApplication.instance().quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.offset = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def change_state(self, state):
        if state == 'idle':
            self.movie = QMovie('./assets/idle.gif')  # 替换为您的动图路径
        elif state == 'happy':
            self.movie = QMovie('./assets/sing.gif')  # 替换为您的动图路径
        elif state == 'sad':
            self.movie = QMovie('./assets/chonglang.gif')  # 替换为您的动图路径
        elif state == 'eat':
            self.movie = QMovie('./assets/eat.gif')  # 替换为您的动图路径

        # 使动图适应QLabel大小
        self.movie.setScaledSize(QSize(self.label.width(), self.label.height()))
        self.label.setMovie(self.movie)
        self.movie.start()

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        # 添加菜单项
        happy_action = QAction('开心', self)
        sad_action = QAction('冲浪', self)
        eat_action = QAction('吃东西', self)
        idle_action = QAction('空闲', self)

        happy_action.triggered.connect(lambda: self.change_state('happy'))
        sad_action.triggered.connect(lambda: self.change_state('sad'))
        eat_action.triggered.connect(lambda: self.change_state('eat'))
        idle_action.triggered.connect(lambda: self.change_state('idle'))

        context_menu.addAction(happy_action)
        context_menu.addAction(sad_action)
        context_menu.addAction(eat_action)
        context_menu.addAction(idle_action)

        # 设置 QMenu 的样式
        context_menu.setStyleSheet(""" 
                QMenu {
                    background-color: white;  /* 背景色为白色 */
                    border: 1px solid light gray; /* 边框 */
                    border-radius: 10px;           /* 圆角半径 */
                    width: 100px;              /* 设置最小宽度 */
                    text-align: center; /* 字体居中 */
                }
                QMenu::item {
                    width: 100px;     
                    padding: 8px ;  /* 菜单项内边距 */
                    color: black;       /* 字体颜色 */
                    text-align: center; /* 字体居中 */
                    border-radius: 5px;            /* 菜单项圆角 */
                }
                QMenu::item:selected {
                    background-color: #f0f0f0; /* 鼠标悬停背景色 */
                }
            """)

        context_menu.exec_(self.mapToGlobal(pos))

    def dragEnterEvent(self, event):
        # 如果拖入的是文件，则接受拖放操作
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 处理拖放事件
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    print(file_path)
                    thread1 = Thread(target=self.process_file_in_thread, args=(file_path,))
                    thread1.start()

    def process_file_in_thread(self, file_path):
        from filetool import process_file  # 确保导入不会阻塞主线程
        message = process_file(file_path)
        # 处理完成后发送信号
        self.file_signal_emitter.file_processed.emit(file_path)

    def on_file_processed(self, message):
        # 显示文件处理完成的提示
        QMessageBox.information(self, "文件处理完成",message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用程序图标（替换为您的图标路径）
    app.setWindowIcon(QIcon("assets/icon.ico"))

    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())
