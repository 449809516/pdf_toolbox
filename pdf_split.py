#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_dir):
    """
    拆分PDF文件的每一页为单独的PDF文件
    """
    try:
        # 读取PDF文件
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 创建输出目录
        output_folder = os.path.join(output_dir, f"{base_name}_split")
        os.makedirs(output_folder, exist_ok=True)
        
        # 拆分每一页
        for page_num in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            
            output_path = os.path.join(output_folder, f"{base_name}_page_{page_num + 1}.pdf")
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        return f"PDF拆分完成！共拆分 {total_pages} 页，文件保存在: {output_folder}"
        
    except Exception as e:
        raise Exception(f"PDF拆分失败: {str(e)}")

def split_pdf_by_range(input_path, output_dir, page_ranges):
    """
    按指定范围拆分PDF文件
    page_ranges: 例如 ["1-3", "5-7", "9-12"]
    """
    try:
        reader = PdfReader(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        for i, page_range in enumerate(page_ranges):
            writer = PdfWriter()
            
            if '-' in page_range:
                start, end = map(int, page_range.split('-'))
                for page_num in range(start - 1, end):
                    writer.add_page(reader.pages[page_num])
            else:
                page_num = int(page_range) - 1
                writer.add_page(reader.pages[page_num])
            
            output_path = os.path.join(output_dir, f"{base_name}_part_{i + 1}.pdf")
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        return f"PDF按范围拆分完成！共生成 {len(page_ranges)} 个文件"
        
    except Exception as e:
        raise Exception(f"PDF按范围拆分失败: {str(e)}")
