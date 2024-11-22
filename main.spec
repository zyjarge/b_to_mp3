# -*- mode: python ; coding: utf-8 -*-

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
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DownloaderApp',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='res/mp3.icns',
)
app = BUNDLE(
    exe,
    name='DownloaderApp.app',
    icon='res/mp3.icns',
    bundle_identifier=None,
)
