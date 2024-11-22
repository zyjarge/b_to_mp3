import json
import os
import sys

def get_resource_path(relative_path):
    """获取资源文件的正确路径，兼容开发环境和打包后的环境"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的路径
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_config():
    config_path = get_resource_path(os.path.join('res', 'config.json'))
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载配置文件失败: {e}")
    
    # 如果配置文件不存在或加载失败，返回默认配置
    return {'download_path': '', 'download_type': 'audio'}

def save_config(config):
    try:
        # 获取应用程序所在目录
        if getattr(sys, 'frozen', False):
            # 打包后的应用程序目录
            app_dir = os.path.dirname(sys.executable)
        else:
            # 开发环境下的目录
            app_dir = os.path.abspath(".")
        
        # 确保 res 目录存在
        res_dir = os.path.join(app_dir, 'res')
        os.makedirs(res_dir, exist_ok=True)
        
        # 保存配置文件
        config_path = os.path.join(res_dir, 'config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"保存配置文件失败: {e}") 