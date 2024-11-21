import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import io
import sys
import os
import subprocess
from downloader_logic import Downloader
import config

class DownloaderApp:
    def __init__(self, root, config_data):
        self.root = root
        self.root.title("B站视频下载器")
        self.config = config_data

        # 下载路径
        self.download_path = tk.StringVar(value=self.config['download_path'])
        self.download_type = tk.StringVar(value=self.config.get('download_type', 'audio'))

        # 创建界面
        self.create_widgets()

        # 重定向标准输出到文本框
        self.redirect_output()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(top_frame, text="下载路径:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(top_frame, textvariable=self.download_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="we", columnspan=2)
        tk.Button(top_frame, text="选择路径", command=self.select_path).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(top_frame, text="打开下载路径", command=self.open_download_path).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(top_frame, text="下载类型:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        radio_frame = tk.Frame(top_frame)
        radio_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        audio_radio = tk.Radiobutton(radio_frame, text="音频", variable=self.download_type, value='audio')
        video_radio = tk.Radiobutton(radio_frame, text="视频", variable=self.download_type, value='video')
        both_radio = tk.Radiobutton(radio_frame, text="音频+视频", variable=self.download_type, value='both')
        audio_radio.pack(side=tk.LEFT)
        video_radio.pack(side=tk.LEFT)
        both_radio.pack(side=tk.LEFT)

        tk.Label(top_frame, text="视频链接:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.url_text = scrolledtext.ScrolledText(top_frame, height=5)
        self.url_text.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="nsew")

        tk.Label(top_frame, text="请输入视频链接，每行一个URL").grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # 调整下载按钮的宽度和高度
        download_button = tk.Button(top_frame, text="开始下载", command=self.start_download, height=2)
        download_button.grid(row=4, column=0, columnspan=4, pady=10, sticky="we")

        self.progress_label = tk.Label(top_frame, text="")
        self.progress_label.grid(row=5, column=0, columnspan=4, pady=5, sticky="w")

        # 日志输出和清空日志按钮
        log_frame = tk.Frame(bottom_frame)
        log_frame.pack(fill=tk.X)

        tk.Label(log_frame, text="日志输出:").pack(side=tk.LEFT, anchor="w")
        clear_log_button = tk.Button(log_frame, text="清空日志", command=self.clear_log)
        clear_log_button.pack(side=tk.RIGHT)

        self.log_text = scrolledtext.ScrolledText(bottom_frame, width=80, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 使 top_frame 的列在窗口调整大小时自动扩展
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_rowconfigure(2, weight=1)

    def redirect_output(self):
        class TextRedirector(io.StringIO):
            def __init__(self, text_widget, tag=""):
                self.text_widget = text_widget
                self.tag = tag

            def write(self, str):
                self.text_widget.configure(state="normal")
                self.text_widget.insert(tk.END, str, (self.tag,))
                self.text_widget.see(tk.END)
                self.text_widget.configure(state="disabled")

        sys.stdout = TextRedirector(self.log_text, "stdout")
        sys.stderr = TextRedirector(self.log_text, "stderr")

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.download_path.set(path)
            self.config['download_path'] = path
            config.save_config(self.config)

    def open_download_path(self):
        path = self.download_path.get()
        if os.path.isdir(path):
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        else:
            messagebox.showerror("错误", "下载路径无效")

    def start_download(self):
        urls = self.url_text.get("1.0", tk.END).strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        if not urls or not self.download_path.get():
            messagebox.showwarning("警告", "请填写所有必填项")
            return

        # 保存下载类型到配置
        self.config['download_type'] = self.download_type.get()
        config.save_config(self.config)

        downloader = Downloader(self.download_path.get(), self.download_type.get(), self.update_progress)
        threading.Thread(target=downloader.download_videos, args=(urls,)).start()

    def update_progress(self, message):
        self.progress_label.config(text=message)

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state="disabled")
