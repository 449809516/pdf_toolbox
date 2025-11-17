# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(5000)  # 解决递归深度问题

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],  # 当前目录
    binaries=[],
    datas=[],  # 不需要额外数据文件
    hiddenimports=[
        # PyQt5相关
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
        
        # 项目模块
        'ui',
        'pdf_split',
        'pdf_merge', 
        'pdf_to_image',
        'pdf_image_extract',
        'pdf_table_extract',
        'pdf_text_extract',
        'image_to_pdf',
        'batch_print',
        'pdf_protect',
        'pdf_preview',
        
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
        'tkinter',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF工具箱',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='pdf_icon.ico',
)
