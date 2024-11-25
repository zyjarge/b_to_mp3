# -*- mode: python ; coding: utf-8 -*-

block_cipher = None  # 添加这行
# 添加 ffmpeg 和 ffprobe 的路径
ffmpeg_path = '/usr/local/bin/ffmpeg'  # 根据实际路径修改
ffprobe_path = '/usr/local/bin/ffprobe'  # 根据实际路径修改

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[
        (ffmpeg_path, '.'),  # 将 ffmpeg 添加到根目录
        (ffprobe_path, '.'),  # 将 ffprobe 添加到根目录
    ],
    datas=[
        ('res/config.json', 'res'),
        ('res/mp3.icns', 'res')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,  # 重要：使用onedir模式
    name='DownloaderApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='res/mp3.icns'
)

# 收集所有文件到一个目录
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DownloaderApp'
)

# 创建macOS应用程序包
app = BUNDLE(
    coll,  # 使用COLLECT的输出
    name='DownloaderApp.app',
    icon='res/mp3.icns',
    bundle_identifier=None,
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    }
)
