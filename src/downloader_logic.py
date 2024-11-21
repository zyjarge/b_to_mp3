import yt_dlp
import os
import re

class Downloader:
    def __init__(self, download_path, download_type='audio', progress_callback=None):
        self.download_path = download_path
        self.download_type = download_type
        self.progress_callback = progress_callback

    def process_url(self, url):
        match = re.match(r'(https?://(?:www\.)?bilibili\.com/video/[A-Za-z0-9]+)', url)
        if match:
            return match.group(1)
        return url

    def download_video(self, url, download_type):
        ydl_opts = {
            'outtmpl': f"{self.download_path}/%(title)s.%(ext)s",
            'progress_hooks': [self.progress_hook],
        }

        if download_type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif download_type == 'video':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_videos(self, urls):
        for url in urls:
            processed_url = self.process_url(url)
            if self.download_type == 'both':
                self.download_video(processed_url, 'audio')
                self.download_video(processed_url, 'video')
            else:
                self.download_video(processed_url, self.download_type)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            message = f"下载进度: {d['_percent_str']} 速度: {d['_speed_str']}"
            print(message)
            if self.progress_callback:
                self.progress_callback(message)
        elif d['status'] == 'finished':
            message = "下载完成"
            print(message)
            if self.progress_callback:
                self.progress_callback(message)

def run_cli_mode(config):
    downloader = Downloader(config['download_path'])
    urls = input("请输入视频链接，每行一个URL，输入完成后按回车：\n").strip().split('\n')
    downloader.download_videos(urls) 