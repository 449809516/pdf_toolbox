#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfReader
import pdfplumber

def extract_text_from_pdf(input_path, output_dir):
    """
    从PDF文件中提取文本内容
    """
    try:
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 输出文件路径
        output_path = os.path.join(output_dir, f"{base_name}_extracted_text.txt")
        
        # 方法1: 使用PyPDF2提取文本
        text_pypdf2 = ""
        with open(input_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text_pypdf2 += page.extract_text() + "\n\n"
        
        # 方法2: 使用pdfplumber提取文本（通常更准确）
        text_pdfplumber = ""
        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pdfplumber += page_text + "\n\n"
        
        # 选择更好的提取结果
        if len(text_pdfplumber.strip()) > len(text_pypdf2.strip()):
            final_text = text_pdfplumber
            method = "pdfplumber"
        else:
            final_text = text_pypdf2
            method = "PyPDF2"
        
        # 保存文本文件
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(final_text)
        
        # 统计信息
        char_count = len(final_text)
        word_count = len(final_text.split())
        line_count = len(final_text.split('\n'))
        
        return f"文本提取完成！使用{method}方法，共提取{char_count}字符，{word_count}单词，{line_count}行。文件保存为: {output_path}"
        
    except Exception as e:
        raise Exception(f"文本提取失败: {str(e)}")

def extract_text_by_pages(input_path, output_dir):
    """
    按页提取文本，每页保存为一个文件
    """
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_folder = os.path.join(output_dir, f"{base_name}_text_pages")
        os.makedirs(output_folder, exist_ok=True)
        
        with pdfplumber.open(input_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    output_path = os.path.join(output_folder, f"{base_name}_page_{page_num + 1}.txt")
                    with open(output_path, 'w', encoding='utf-8') as text_file:
                        text_file.write(text)
        
        return f"按页文本提取完成！文件保存在: {output_folder}"
        
    except Exception as e:
        raise Exception(f"按页文本提取失败: {str(e)}")
