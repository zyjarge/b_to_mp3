import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QRadioButton, QButtonGroup, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QMetaType, pyqtSlot
import threading
import os
import subprocess
from downloader_logic import Downloader
import config
from PyQt5.QtGui import QTextCursor

class PyQtDownloaderApp(QWidget):
    def __init__(self, config_data):
        super().__init__()
        self.config = config_data

        # 下载路径
        self.download_path = self.config.get('download_path', '')
        self.download_type = self.config.get('download_type', 'audio')

        # 在应用程序启动时注册QTextCursor类型
        QMetaType.registerType("QTextCursor")

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PyQt B站视频下载器")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 下载路径
        path_layout = QHBoxLayout()
        path_label = QLabel("下载路径:")
        self.path_edit = QLineEdit(self.download_path)
        select_path_button = QPushButton("选择路径")
        open_path_button = QPushButton("打开下载路径")
        select_path_button.clicked.connect(self.select_path)
        open_path_button.clicked.connect(self.open_download_path)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(select_path_button)
        path_layout.addWidget(open_path_button)

        # 下载类型
        type_layout = QHBoxLayout()
        type_label = QLabel("下载类型:")
        self.audio_radio = QRadioButton("音频")
        self.video_radio = QRadioButton("视频")
        self.both_radio = QRadioButton("音频+视频")
        self.audio_radio.setChecked(self.download_type == 'audio')
        self.video_radio.setChecked(self.download_type == 'video')
        self.both_radio.setChecked(self.download_type == 'both')

        self.type_group = QButtonGroup()
        self.type_group.addButton(self.audio_radio)
        self.type_group.addButton(self.video_radio)
        self.type_group.addButton(self.both_radio)

        type_layout.addWidget(type_label)
        type_layout.addWidget(self.audio_radio)
        type_layout.addWidget(self.video_radio)
        type_layout.addWidget(self.both_radio)

        # 视频链接
        link_label = QLabel("视频链接:")
        self.link_text = QTextEdit()
        link_hint_label = QLabel("请输入视频链接，每行一个URL")

        # 下载按钮
        download_button = QPushButton("开始下载")
        download_button.clicked.connect(self.start_download)

        # 进度显示
        self.progress_label = QLabel("")

        # 日志输出
        log_label = QLabel("日志输出:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        clear_log_button = QPushButton("清空日志")
        clear_log_button.clicked.connect(self.clear_log)

        # 布局
        layout.addLayout(path_layout)
        layout.addLayout(type_layout)
        layout.addWidget(link_label)
        layout.addWidget(self.link_text)
        layout.addWidget(link_hint_label)
        layout.addWidget(download_button)
        layout.addWidget(self.progress_label)
        layout.addWidget(log_label)
        layout.addWidget(self.log_text)
        layout.addWidget(clear_log_button)

        self.setLayout(layout)

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择下载路径", self.download_path)
        if path:
            self.download_path = path
            self.path_edit.setText(path)
            self.config['download_path'] = path
            config.save_config(self.config)

    def open_download_path(self):
        path = self.download_path
        if os.path.isdir(path):
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        else:
            QMessageBox.critical(self, "错误", "下载路径无效")

    def start_download(self):
        urls = self.link_text.toPlainText().strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        if not urls or not self.download_path:
            QMessageBox.warning(self, "警告", "请填写所有必填项")
            return

        # 保存下载类型到配置
        if self.audio_radio.isChecked():
            self.download_type = 'audio'
        elif self.video_radio.isChecked():
            self.download_type = 'video'
        elif self.both_radio.isChecked():
            self.download_type = 'both'

        self.config['download_type'] = self.download_type
        config.save_config(self.config)

        downloader = Downloader(self.download_path, self.download_type, self.update_progress)
        threading.Thread(target=downloader.download_videos, args=(urls,)).start()

    def update_progress(self, message):
        self.progress_label.setText(message)
        self.log_text.append(message)

    def clear_log(self):
        self.log_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config_data = config.load_config()
    window = PyQtDownloaderApp(config_data)
    window.show()
    sys.exit(app.exec_()) 