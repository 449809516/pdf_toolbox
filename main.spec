# -*- mode: python ; coding: utf-8 -*-

import sys
# 增加递归深度限制
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['E:/pdf 豆包/pdf_toolbox'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # PyQt5相关
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
        
        # PDF处理相关
        'PyPDF2', 'PyPDF2._utils', 'PyPDF2.pdf',
        'pdf2image', 'pdf2image.pdf2image',
        'pdfplumber', 'pdfplumber.pdf', 'pdfplumber.table',
        'camelot', 'camelot.io', 'camelot.handlers', 'camelot.parsers',
        'img2pdf',
        
        # 图像处理相关
        'PIL', 'PIL.Image', 'PIL.ImageFile', 'PIL._imaging',
        'pytesseract',
        'cv2', 'cv2.cv2',
        
        # 报告生成
        'reportlab', 'reportlab.pdfgen', 'reportlab.lib', 'reportlab.pdfbase',
        
        # 其他必要模块
        'numpy', 'pandas',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',  # 排除不需要的模块
        'test',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF工具箱',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 先关闭UPX压缩，避免其他问题
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='pdf_icon.ico',
)
