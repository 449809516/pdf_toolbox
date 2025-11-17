#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import img2pdf
from PIL import Image

def images_to_pdf(image_paths, output_path):
    """
    将多张图片合并为一个PDF文件
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 验证所有图片文件是否存在
        for img_path in image_paths:
            if not os.path.exists(img_path):
                raise Exception(f"图片文件不存在: {img_path}")
        
        # 使用img2pdf库转换
        with open(output_path, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(image_paths))
        
        return f"图片转PDF完成！共转换 {len(image_paths)} 张图片，输出文件: {output_path}"
        
    except Exception as e:
        raise Exception(f"图片转PDF失败: {str(e)}")

def images_to_pdf_pillow(image_paths, output_path, size=None):
    """
    使用Pillow库将图片转换为PDF
    """
    try:
        images = []
        
        for img_path in image_paths:
            # 打开图片
            img = Image.open(img_path)
            
            # 转换为RGB模式（如果需要）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整大小（如果指定）
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            images.append(img)
        
        # 保存为PDF
        if images:
            images[0].save(
                output_path, 
                "PDF", 
                save_all=True, 
                append_images=images[1:]
            )
        
        return f"图片转PDF完成！共转换 {len(images)} 张图片"
        
    except Exception as e:
        raise Exception(f"图片转PDF失败: {str(e)}")

def folder_images_to_pdf(folder_path, output_path, image_extensions=None):
    """
    将文件夹中的所有图片转换为一个PDF文件
    """
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    try:
        # 获取文件夹中所有图片文件
        image_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(folder_path, file))
        
        if not image_files:
            raise Exception("文件夹中没有找到支持的图片文件")
        
        # 按文件名排序
        image_files.sort()
        
        # 转换为PDF
        return images_to_pdf(image_files, output_path)
        
    except Exception as e:
        raise Exception(f"文件夹图片转PDF失败: {str(e)}")
