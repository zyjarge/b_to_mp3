import sys
import tkinter as tk
from DownloaderApp import DownloaderApp
from downloader_logic import run_cli_mode
import config
import argparse

def main():
    parser = argparse.ArgumentParser(description="B站视频下载器")
    parser.add_argument('--cli', action='store_true', help='以命令行模式运行')
    args = parser.parse_args()

    config_data = config.load_config()

    if args.cli:
        run_cli_mode(config_data)
    else:
        root = tk.Tk()
        app = DownloaderApp(root, config_data)
        root.mainloop()

if __name__ == "__main__":
    main() 