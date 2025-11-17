#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def check_files():
    """检查所有必需文件是否存在"""
    required_files = [
        'main.py',
        'ui.py',
        'pdf_split.py',
        'pdf_merge.py',
        'pdf_to_image.py',
        'pdf_image_extract.py',
        'pdf_table_extract.py',
        'pdf_text_extract.py',
        'image_to_pdf.py',
        'batch_print.py',
        'pdf_protect.py',
        'pdf_preview.py',
        'pdf_icon.ico',
        'requirements.txt'
    ]
    
    print("检查项目文件...")
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - 缺失")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n错误: 缺少 {len(missing_files)} 个文件")
        return False
    return True

def install_requirements():
    """安装依赖包"""
    print("\n安装依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False

def build_exe():
    """打包exe"""
    print("\n开始打包...")
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "pdf_toolbox.spec"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False

def main():
    print("=" * 50)
    print("          PDF工具箱打包程序")
    print("=" * 50)
    
    # 检查文件
    if not check_files():
        input("按回车键退出...")
        return
    
    # 安装依赖
    if not install_requirements():
        input("按回车键退出...")
        return
    
    # 打包
    if build_exe():
        print("\n" + "=" * 50)
        print("           打包成功！")
        print("=" * 50)
        print("可执行文件位置: dist/PDF工具箱.exe")
        print("\n请将以下文件一起分发:")
        print("  - PDF工具箱.exe")
        print("  - README.txt")
        print("\n注意: 用户需要安装Poppler工具用于PDF转图片功能")
    else:
        print("\n打包失败！")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
