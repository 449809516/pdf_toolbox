#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from pdf2image import convert_from_path
from PIL import Image

def find_poppler_path():
    """
    动态查找Poppler的bin目录
    尝试多个常见安装位置
    """
    # 常见的Poppler安装路径列表
    possible_paths = [
        r'C:\poppler\Library\bin',                # 我们推荐的路径
        r'C:\poppler\bin',                       # 可能的解压路径
        r'C:\Program Files\poppler\Library\bin', # 程序文件目录
        r'C:\Program Files (x86)\poppler\Library\bin',
        r'D:\poppler\Library\bin',              # D盘可能的路径
    ]
    
    # 尝试每个可能的路径
    for path in possible_paths:
        if os.path.exists(path):
            # 检查是否包含必要的可执行文件
            required_files = ['pdftoppm.exe', 'pdftocairo.exe']
            if all(os.path.exists(os.path.join(path, f)) for f in required_files):
                print(f"找到Poppler路径: {path}")
                return path
    
    print("未找到有效的Poppler路径")
    return None

# 自动检测Poppler路径，如果找不到则使用None（尝试使用系统PATH）
POPPLER_PATH = find_poppler_path()

def pdf_to_images(input_path, output_dir, dpi=200, fmt='PNG'):
    """
    将PDF文件的每一页转换为图片
    """
    try:
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 转换PDF为图片，传入poppler路径
        images = convert_from_path(input_path, dpi=dpi, poppler_path=POPPLER_PATH)
        
        # 直接在原文件所在目录保存图片，不创建子文件夹
        saved_files = []
        for i, image in enumerate(images):
            output_path = os.path.join(output_dir, f"{base_name}_page_{i + 1}.{fmt.lower()}")
            image.save(output_path, fmt.upper())
            saved_files.append(output_path)
        
        return f"PDF转图片完成！共转换 {len(images)} 页，文件已直接保存在原PDF文件旁边"
        
    except Exception as e:
        error_msg = str(e)
        # 针对Poppler未找到的错误，提供更详细的提示
        if "Unable to get page count" in error_msg or "poppler" in error_msg.lower():
            detected_path_info = f"检测到的Poppler路径: {POPPLER_PATH}" if POPPLER_PATH else "未检测到Poppler路径"
            raise Exception(f"PDF转图片失败: {error_msg}\n\n{detected_path_info}\n\n"  
                           "请按照以下步骤安装和配置Poppler:\n"  
                           "1. 访问 https://github.com/oschwartz10612/poppler-windows/releases/ 下载Poppler\n"  
                           "2. 解压到 C:\\poppler 目录，确保目录结构为 C:\\poppler\\Library\\bin\n"  
                           "3. 确认bin目录中包含 pdftoppm.exe 和 pdftocairo.exe 两个文件\n"  
                           "4. 完成后重启程序，系统将自动检测Poppler")
        else:
            raise Exception(f"PDF转图片失败: {error_msg}")

def pdf_to_images_custom(input_path, output_dir, dpi=200, fmt='PNG', 
                        quality=95, size=None):
    """
    自定义参数的PDF转图片功能
    size: 可选，指定图片大小 (width, height)
    """
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 转换PDF为图片，传入poppler路径
        images = convert_from_path(input_path, dpi=dpi, poppler_path=POPPLER_PATH)
        
        for i, image in enumerate(images):
            # 调整图片大小（如果指定）
            if size:
                image = image.resize(size, Image.Resampling.LANCZOS)
            
            # 直接在原文件所在目录保存图片，不创建子文件夹
            output_path = os.path.join(output_dir, f"{base_name}_page_{i + 1}.{fmt.lower()}")
            
            # 根据格式保存
            if fmt.upper() == 'JPEG':
                image.save(output_path, 'JPEG', quality=quality)
            else:
                image.save(output_path, fmt.upper())
        
        return f"PDF转图片完成！共转换 {len(images)} 页，文件已直接保存在原PDF文件旁边"
        
    except Exception as e:
        error_msg = str(e)
        # 针对Poppler未找到的错误，提供更详细的提示
        if "Unable to get page count" in error_msg or "poppler" in error_msg.lower():
            detected_path_info = f"检测到的Poppler路径: {POPPLER_PATH}" if POPPLER_PATH else "未检测到Poppler路径"
            raise Exception(f"PDF转图片失败: {error_msg}\n\n{detected_path_info}\n\n"  
                           "请按照以下步骤安装和配置Poppler:\n"  
                           "1. 访问 https://github.com/oschwartz10612/poppler-windows/releases/ 下载Poppler\n"  
                           "2. 解压到 C:\\poppler 目录，确保目录结构为 C:\\poppler\\Library\\bin\n"  
                           "3. 确认bin目录中包含 pdftoppm.exe 和 pdftocairo.exe 两个文件\n"  
                           "4. 完成后重启程序，系统将自动检测Poppler")
        else:
            raise Exception(f"PDF转图片失败: {error_msg}")