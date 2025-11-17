#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pdfplumber
import pandas as pd

def extract_tables_from_pdf(input_path, output_dir):
    """
    从PDF文件中提取表格
    """
    try:
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # 创建输出目录
        output_folder = os.path.join(output_dir, f"{base_name}_tables")
        os.makedirs(output_folder, exist_ok=True)
        
        table_count = 0
        
        with pdfplumber.open(input_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # 提取表格
                tables = page.extract_tables()
                
                for table_num, table in enumerate(tables):
                    if table and len(table) > 1:  # 确保表格有数据
                        # 转换为DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        # 保存为Excel文件
                        excel_filename = f"{base_name}_page_{page_num + 1}_table_{table_num + 1}.xlsx"
                        excel_path = os.path.join(output_folder, excel_filename)
                        df.to_excel(excel_path, index=False)
                        
                        # 同时保存为CSV文件
                        csv_filename = f"{base_name}_page_{page_num + 1}_table_{table_num + 1}.csv"
                        csv_path = os.path.join(output_folder, csv_filename)
                        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                        
                        table_count += 1
        
        return f"表格提取完成！共提取 {table_count} 个表格，文件保存在: {output_folder}"
        
    except Exception as e:
        raise Exception(f"表格提取失败: {str(e)}")

def extract_tables_with_camelot(input_path, output_dir):
    """
    使用Camelot库提取表格（需要安装camelot-py和ghostscript）
    """
    try:
        import camelot
        
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_folder = os.path.join(output_dir, f"{base_name}_tables_camelot")
        os.makedirs(output_folder, exist_ok=True)
        
        # 使用Camelot提取表格
        tables = camelot.read_pdf(input_path, pages='all')
        
        table_count = 0
        for i, table in enumerate(tables):
            if table.parsing_report['accuracy'] > 50:  # 准确率阈值
                # 保存为Excel
                excel_filename = f"{base_name}_table_{i + 1}.xlsx"
                excel_path = os.path.join(output_folder, excel_filename)
                table.df.to_excel(excel_path, index=False)
                
                # 保存为CSV
                csv_filename = f"{base_name}_table_{i + 1}.csv"
                csv_path = os.path.join(output_folder, csv_filename)
                table.df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                
                table_count += 1
        
        return f"Camelot表格提取完成！共提取 {table_count} 个表格"
        
    except ImportError:
        raise Exception("请安装camelot-py: pip install camelot-py[base]")
    except Exception as e:
        raise Exception(f"Camelot表格提取失败: {str(e)}")
