#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess
from pdf2image import convert_from_path

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

def preview_pdf(input_path, output_dir=None, pages=None, dpi=150):
    """
    生成PDF文件的预览图片
    """
    try:
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 如果没有指定输出目录，使用临时目录
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        
        # 创建输出目录
        output_folder = os.path.join(output_dir, f"{base_name}_preview")
        os.makedirs(output_folder, exist_ok=True)
        
        # 转换PDF为图片
        print(f"正在尝试使用Poppler路径: {POPPLER_PATH}")
        print(f"检查路径是否存在: {os.path.exists(POPPLER_PATH) if POPPLER_PATH else '使用系统PATH'}")
        if POPPLER_PATH and os.path.exists(POPPLER_PATH):
            print(f"Poppler路径内容: {os.listdir(POPPLER_PATH)[:5]}...")
        
        if pages:
            images = convert_from_path(input_path, dpi=dpi, first_page=pages[0], last_page=pages[1], poppler_path=POPPLER_PATH)
        else:
            images = convert_from_path(input_path, dpi=dpi, poppler_path=POPPLER_PATH)  # 传入poppler路径
        
        # 保存预览图片
        preview_files = []
        for i, image in enumerate(images):
            output_path = os.path.join(output_folder, f"{base_name}_preview_{i + 1}.jpg")
            image.save(output_path, 'JPEG', quality=85)
            preview_files.append(output_path)
        
        # 打开第一张预览图片
        if preview_files:
            open_preview_image(preview_files[0])
        
        return f"PDF预览生成完成！共生成 {len(images)} 张预览图片"
        
    except Exception as e:
        error_msg = str(e)
        # 检测是否是Poppler未找到的错误
        if "Unable to get page count" in error_msg or "poppler" in error_msg.lower():
            detected_path_info = f"检测到的Poppler路径: {POPPLER_PATH}" if POPPLER_PATH else "未检测到Poppler路径"
            raise Exception(
                f"PDF预览失败: {error_msg}\n\n"  
                f"{detected_path_info}\n\n"  
                "请按照以下步骤安装和配置Poppler:\n"  
                "1. 访问 https://github.com/oschwartz10612/poppler-windows/releases/ 下载Poppler\n"  
                "2. 解压到 C:\\poppler 目录，确保目录结构为 C:\\poppler\\Library\\bin\n"  
                "3. 确认bin目录中包含 pdftoppm.exe 和 pdftocairo.exe 两个文件\n"  
                "4. 完成后重启程序，系统将自动检测Poppler"
            )
        raise Exception(f"PDF预览失败: {error_msg}")

def open_preview_image(image_path):
    """
    打开预览图片
    """
    try:
        import platform
        system = platform.system()
        
        if system == "Windows":
            os.startfile(image_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", image_path])
        else:  # Linux
            subprocess.run(["xdg-open", image_path])
        
        return True
        
    except Exception as e:
        raise Exception(f"打开预览图片失败: {str(e)}")

def get_pdf_info(input_path):
    """
    获取PDF文件的基本信息
    """
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(input_path)
        info = reader.metadata
        
        result = {
            '页数': len(reader.pages),
            '标题': getattr(info, 'title', '未知'),
            '作者': getattr(info, 'author', '未知'),
            '创建者': getattr(info, 'creator', '未知'),
            '制作工具': getattr(info, 'producer', '未知'),
            '创建日期': getattr(info, 'creation_date', '未知'),
            '修改日期': getattr(info, 'modification_date', '未知'),
            '是否加密': reader.is_encrypted
        }
        
        info_text = "PDF文件信息:\n"
        for key, value in result.items():
            info_text += f"{key}: {value}\n"
        
        return info_text
        
    except Exception as e:
        raise Exception(f"获取PDF信息失败: {str(e)}")