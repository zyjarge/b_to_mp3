import os
import sys
from yt_dlp import YoutubeDL

def run_cli_mode(config):
    """命令行模式运行下载器"""
    print("请输入视频链接，每行一个URL，输入完成后按回车：")
    urls = input().strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()]
    
    if not urls:
        print("未输入任何URL")
        return
        
    if not config.get('download_path'):
        print("错误：未设置下载路径")
        return
        
    downloader = Downloader(
        config['download_path'],
        config.get('download_type', 'audio'),
        progress_callback=print  # 使用print作为回调函数
    )
    downloader.download_videos(urls)

class Downloader:
    def __init__(self, download_path, download_type='audio', progress_callback=None):
        self.download_path = download_path
        self.download_type = download_type
        self.progress_callback = progress_callback

    def download_videos(self, urls):
        if not urls:
            return

        # 配置下载选项
        ydl_opts = {
            'format': 'bestaudio/best' if self.download_type == 'audio' else 'best',
            'paths': {'home': self.download_path},
            'progress_hooks': [self.progress_hook] if self.progress_callback else [],  # 改为空列表而不是None
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