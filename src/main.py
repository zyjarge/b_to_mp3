import sys
import tkinter as tk
from tkinter import messagebox
from DownloaderApp import DownloaderApp
import config
import argparse
import traceback

def main():
    try:
        parser = argparse.ArgumentParser(description="B站视频下载器")
        parser.add_argument('--cli', action='store_true', help='以命令行模式运行')
        args = parser.parse_args()

        config_data = config.load_config()

        if args.cli:
            from downloader_logic import run_cli_mode
            run_cli_mode(config_data)
        else:
            root = tk.Tk()
            app = DownloaderApp(root, config_data)
            root.mainloop()
    except ImportError as e:
        error_msg = f"导入错误: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        if not getattr(args, 'cli', False):
            messagebox.showerror("错误", error_msg)
    except Exception as e:
        error_msg = f"发生错误: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        if not getattr(args, 'cli', False):
            messagebox.showerror("错误", error_msg)

if __name__ == "__main__":
    main() 