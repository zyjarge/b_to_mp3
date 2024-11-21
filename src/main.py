import sys
import tkinter as tk
from DownloaderApp import DownloaderApp
from downloader_logic import run_cli_mode
import config

def main():
    config_data = config.load_config()

    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli_mode(config_data)
    else:
        root = tk.Tk()
        app = DownloaderApp(root, config_data)
        root.mainloop()

if __name__ == "__main__":
    main() 