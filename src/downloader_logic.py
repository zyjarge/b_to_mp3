import os
import sys
from yt_dlp import YoutubeDL

def run_cli_mode(config):
    downloader = Downloader(config['download_path'])
    urls = input("请输入视频链接，每行一个URL，输入完成后按回车：\n").strip().split('\n')
    downloader.download_videos(urls)

class Downloader:
    def __init__(self, download_path, download_type='audio', progress_callback=None):
        self.download_path = download_path
        self.download_type = download_type
        self.progress_callback = progress_callback

    def download_videos(self, urls):
        if not urls:
            return

        # 获取 ffmpeg 路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的应用
            base_path = sys._MEIPASS
        else:
            # 如果是开发环境
            base_path = os.path.abspath(".")

        ffmpeg_location = os.path.join(base_path, 'ffmpeg')
        
        # 配置下载选项
        ydl_opts = {
            'format': 'bestaudio/best' if self.download_type == 'audio' else 'best',
            'paths': {'home': self.download_path},
            'ffmpeg_location': base_path,  # 设置 ffmpeg 路径
            'progress_hooks': [self.progress_hook] if self.progress_callback else None,
        }

        # 根据下载类型设置后处理器
        if self.download_type == 'audio':
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            })

        # 开始下载
        with YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                try:
                    ydl.download([url])
                except Exception as e:
                    if self.progress_callback:
                        self.progress_callback(f"下载失败: {str(e)}")

    def progress_hook(self, d):
        if self.progress_callback:
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                self.progress_callback(f"下载中... {percent} 速度: {speed}")
            elif d['status'] == 'finished':
                self.progress_callback("下载完成，正在处理...") 