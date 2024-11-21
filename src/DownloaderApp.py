import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import yt_dlp
import io
import sys
import re

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("B站视频下载器")

        # 下载路径
        self.download_path = tk.StringVar()
        self.audio_format = tk.StringVar(value='mp3')
        self.video_urls = tk.StringVar()

        # 创建界面
        self.create_widgets()

        # 重定向标准输出到文本框
        self.redirect_output()

    def create_widgets(self):
        # 创建上下分隔的框架
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 上方控件
        # 下载路径选择
        tk.Label(top_frame, text="下载路径:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(top_frame, textvariable=self.download_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(top_frame, text="选择路径", command=self.select_path).grid(row=0, column=2, padx=5, pady=5)

        # 音频格式选择
        tk.Label(top_frame, text="音频格式:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(top_frame, textvariable=self.audio_format, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # 视频链接输入
        tk.Label(top_frame, text="视频链接:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.url_text = scrolledtext.ScrolledText(top_frame, width=50, height=5)
        self.url_text.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="w")

        # URL格式提示
        tk.Label(top_frame, text="请输入视频链接，每行一个URL").grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # 下载按钮
        tk.Button(top_frame, text="开始下载", command=self.start_download).grid(row=4, column=1, pady=10, sticky="w")

        # 下载进度
        self.progress_label = tk.Label(top_frame, text="")
        self.progress_label.grid(row=5, column=0, columnspan=3, pady=5, sticky="w")

        # 下方日志输出
        tk.Label(bottom_frame, text="日志输出:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(bottom_frame, width=80, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

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

    def start_download(self):
        urls = self.url_text.get("1.0", tk.END).strip().split('\n')
        urls = [self.process_url(url.strip()) for url in urls if url.strip()]
        if not urls or not self.download_path.get():
            messagebox.showwarning("警告", "请填写所有必填项")
            return

        threading.Thread(target=self.download_videos, args=(urls,)).start()

    def process_url(self, url):
        # 使用正则表达式匹配B站视频URL的主要部分
        match = re.match(r'(https?://(?:www\.)?bilibili\.com/video/[A-Za-z0-9]+)', url)
        if match:
            return match.group(1)
        return url  # 如果不匹配B站格式，返回原始URL

    def download_videos(self, urls):
        for url in urls:
            self.progress_label.config(text=f"正在处理: {url}")
            self.download_video(url)
        self.progress_label.config(text="所有下载和音频提取完成")

    def download_video(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{self.download_path.get()}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format.get(),
                'preferredquality': '192',
            }],
            'progress_hooks': [self.progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        self.progress_label.config(text="音频提取完成")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progress_label.config(text=f"下载进度: {d['_percent_str']} 速度: {d['_speed_str']}")
        elif d['status'] == 'finished':
            self.progress_label.config(text="视频下载完成，正在提取音频...")
        elif d['status'] == 'error':
            self.progress_label.config(text="下载出错")

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
