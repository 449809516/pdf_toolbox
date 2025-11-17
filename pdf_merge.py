#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfMerger

def merge_pdfs(input_paths, output_path):
    """
    合并多个PDF文件为一个PDF文件
    """
    try:
        merger = PdfMerger()
        
        # 添加所有PDF文件
        for pdf_path in input_paths:
            merger.append(pdf_path)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入合并后的PDF
        with open(output_path, 'wb') as output_file:
            merger.write(output_file)
        
        merger.close()
        
        return f"PDF合并完成！输出文件: {output_path}"
        
    except Exception as e:
        raise Exception(f"PDF合并失败: {str(e)}")

def merge_pdfs_from_folder(folder_path, output_path):
    """
    合并文件夹中的所有PDF文件
    """
    try:
        # 获取文件夹中所有PDF文件
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        pdf_files.sort()  # 按文件名排序
        
        if not pdf_files:
            raise Exception("文件夹中没有找到PDF文件")
        
        input_paths = [os.path.join(folder_path, f) for f in pdf_files]
        
        return merge_pdfs(input_paths, output_path)
        
    except Exception as e:
        raise Exception(f"从文件夹合并PDF失败: {str(e)}")
