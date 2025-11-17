#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fitz  # PyMuPDF
from PIL import Image

def extract_images_from_pdf(input_path, output_dir):
    """
    从PDF文件中提取所有图片
    """
    try:
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 创建输出目录
        output_folder = os.path.join(output_dir, f"{base_name}_extracted_images")
        os.makedirs(output_folder, exist_ok=True)
        
        # 打开PDF文件
        pdf_document = fitz.open(input_path)
        image_count = 0
        
        # 遍历每一页
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                # 获取图片引用
                xref = img[0]
                
                # 提取图片数据
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # 保存图片
                image_filename = f"{base_name}_page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)
                
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                
                image_count += 1
        
        pdf_document.close()
        
        return f"图片提取完成！共提取 {image_count} 张图片，文件保存在: {output_folder}"
        
    except Exception as e:
        raise Exception(f"图片提取失败: {str(e)}")

def extract_images_with_quality(input_path, output_dir, min_width=100, min_height=100):
    """
    提取图片并过滤小图片
    """
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_folder = os.path.join(output_dir, f"{base_name}_extracted_images")
        os.makedirs(output_folder, exist_ok=True)
        
        pdf_document = fitz.open(input_path)
        image_count = 0
        skipped_count = 0
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # 检查图片尺寸
                image_size = base_image["image_size"]
                if image_size[0] >= min_width and image_size[1] >= min_height:
                    image_filename = f"{base_name}_page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                    image_path = os.path.join(output_folder, image_filename)
                    
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_bytes)
                    
                    image_count += 1
                else:
                    skipped_count += 1
        
        pdf_document.close()
        
        return f"图片提取完成！共提取 {image_count} 张图片，跳过 {skipped_count} 张小图片"
        
    except Exception as e:
        raise Exception(f"图片提取失败: {str(e)}")
