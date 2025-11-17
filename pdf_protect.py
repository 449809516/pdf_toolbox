#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfReader, PdfWriter

def protect_pdf(input_path, output_dir, password, owner_password=None):
    """
    为PDF文件添加密码保护
    """
    try:
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 输出文件路径
        output_path = os.path.join(output_dir, f"{base_name}_protected.pdf")
        
        # 读取PDF文件
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # 添加所有页面
        for page in reader.pages:
            writer.add_page(page)
        
        # 添加密码保护
        if owner_password:
            writer.encrypt(user_password=password, owner_password=owner_password,
                          use_128bit=True)
        else:
            writer.encrypt(user_password=password, use_128bit=True)
        
        # 保存加密后的PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return f"PDF保护完成！文件已加密保存为: {output_path}"
        
    except Exception as e:
        raise Exception(f"PDF保护失败: {str(e)}")

def remove_pdf_protection(input_path, output_dir, password):
    """
    移除PDF文件的密码保护
    """
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_unprotected.pdf")
        
        # 读取加密的PDF
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            reader.decrypt(password)
        
        writer = PdfWriter()
        
        # 添加所有页面
        for page in reader.pages:
            writer.add_page(page)
        
        # 保存未加密的PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return f"PDF解密完成！文件已保存为: {output_path}"
        
    except Exception as e:
        raise Exception(f"PDF解密失败: {str(e)}")

def set_pdf_permissions(input_path, output_dir, password, permissions=None):
    """
    设置PDF文件的详细权限
    """
    if permissions is None:
        permissions = {
            'printing': False,           # 禁止打印
            'modifying': False,          # 禁止修改
            'copying': False,            # 禁止复制
            'annotations': False,        # 禁止注释
            'fill_forms': False,         # 禁止填写表单
            'extract': False,            # 禁止提取内容
            'assemble': False            # 禁止组装
        }
    
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_restricted.pdf")
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # 设置权限
        writer.encrypt(
            user_password=password,
            use_128bit=True,
            **permissions
        )
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return f"PDF权限设置完成！文件已保存为: {output_path}"
        
    except Exception as e:
        raise Exception(f"PDF权限设置失败: {str(e)}")
