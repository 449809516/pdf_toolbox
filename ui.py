#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                             QFrame, QTextEdit, QFileDialog, QMessageBox,
                             QProgressBar, QListWidget, QListWidgetItem, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent, QIcon

# 导入功能模块
from pdf_split import split_pdf
from pdf_merge import merge_pdfs
from pdf_to_image import pdf_to_images
from pdf_image_extract import extract_images_from_pdf
from pdf_table_extract import extract_tables_from_pdf
from pdf_text_extract import extract_text_from_pdf
from image_to_pdf import images_to_pdf
from batch_print import batch_print_pdfs
from pdf_protect import protect_pdf
from pdf_preview import preview_pdf

# 工作线程类
class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# 拖拽标签组件
class DropLabel(QLabel):
    fileDropped = pyqtSignal(str)
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            DropLabel {
                border: 3px dashed #aaa;
                border-radius: 10px;
                padding: 40px 20px;
                background-color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                color: #666;
                min-height: 60px;
            }
            DropLabel:hover {
                border-color: #4CAF50;
                background-color: rgba(76, 175, 80, 0.1);
            }
        """)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                DropLabel {
                    border: 3px dashed #4CAF50;
                    border-radius: 10px;
                    padding: 40px 20px;
                    background-color: rgba(76, 175, 80, 0.2);
                    font-size: 14px;
                    color: #666;
                    min-height: 60px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            DropLabel {
                border: 3px dashed #aaa;
                border-radius: 10px;
                padding: 40px 20px;
                background-color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                color: #666;
                min-height: 60px;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet("""
            DropLabel {
                border: 3px dashed #aaa;
                border-radius: 10px;
                padding: 40px 20px;
                background-color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                color: #666;
                min-height: 60px;
            }
        """)
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.pdf'):
                self.fileDropped.emit(file_path)
                break

# 动画按钮组件
class FunctionButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.color = color
        self.setFixedHeight(45)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(self.color)};
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(self.color, 40)};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        
    def darken_color(self, color, amount=20):
        colors = {
            "#FF5722": "#E64A19",
            "#2196F3": "#1976D2",
            "#4CAF50": "#388E3C",
            "#FFC107": "#FFA000",
            "#9C27B0": "#7B1FA2",
            "#00BCD4": "#0097A7",
            "#FF9800": "#F57C00",
            "#795548": "#5D4037",
            "#607D8B": "#455A64",
            "#E91E63": "#C2185B"
        }
        return colors.get(color, color)

# 主窗口
class PDFToolbox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = ""
        self.output_dir = ""
        self.worker_thread = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("PDF工具箱 - 多功能PDF处理工具")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 650)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #f5f7fa, stop: 1 #c3cfe2);
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 12px;
                background-color: white;
                font-size: 13px;
                selection-background-color: #2196F3;
            }
        """)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 左侧功能面板
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # 右侧内容区域
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)
        panel.setMaximumWidth(350)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # 标题
        title = QLabel("PDF工具箱")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2196F3, stop:1 #21CBF3);
                border-radius: 10px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # 拖拽区域
        self.drop_label = DropLabel("📁 拖拽PDF文件到此处\n或点击下方按钮选择文件")
        self.drop_label.fileDropped.connect(self.on_file_dropped)
        layout.addWidget(self.drop_label)
        
        # 文件选择按钮
        file_btn = FunctionButton("选择PDF文件", "#2196F3")
        file_btn.clicked.connect(self.select_file)
        layout.addWidget(file_btn)
        
        # 当前文件显示
        self.file_label = QLabel("未选择文件")
        self.file_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                color: #495057;
                min-height: 40px;
            }
        """)
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 6px;
                text-align: center;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2196F3, stop:1 #21CBF3);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 功能按钮
        functions_label = QLabel("📋 PDF功能")
        functions_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 8px 0;
                border-bottom: 2px solid #2196F3;
            }
        """)
        layout.addWidget(functions_label)
        
        # 功能按钮网格
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # 定义功能按钮
        functions = [
            ("PDF拆分", "#FF5722", self.split_pdf),
            ("PDF合并", "#2196F3", self.merge_pdf),
            ("PDF转图片", "#4CAF50", self.pdf_to_image),
            ("提取图片", "#FFC107", self.extract_images),
            ("提取表格", "#9C27B0", self.extract_tables),
            ("提取文本", "#00BCD4", self.extract_text),
            ("图片转PDF", "#FF9800", self.images_to_pdf),
            ("批量打印", "#795548", self.batch_print),
            ("PDF保护", "#607D8B", self.protect_pdf),
            ("PDF预览", "#E91E63", self.preview_pdf)
        ]
        
        # 添加功能按钮到网格
        for i, (name, color, func) in enumerate(functions):
            btn = FunctionButton(name, color)
            btn.clicked.connect(func)
            grid_layout.addWidget(btn, i // 2, i % 2)
        
        layout.addLayout(grid_layout)
        layout.addStretch()
        
        return panel
        
    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 状态标题
        status_title = QLabel("📊 操作状态")
        status_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                padding-bottom: 10px;
                border-bottom: 2px solid #e9ecef;
            }
        """)
        layout.addWidget(status_title)
        
        # 状态显示区域
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                background-color: #f8f9fa;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.status_display)
        
        # 初始状态消息
        welcome_msg = """
✨ 欢迎使用PDF工具箱！ ✨

📖 使用说明：
1. 拖拽或选择PDF文件
2. 点击功能按钮执行操作
3. 查看右侧状态信息

💡 特点：
• 所有输出文件保存在原文件同目录
• 支持批量操作
• 无需弹窗提示，操作状态实时显示

🚀 开始使用：请先选择一个PDF文件
        """
        self.status_display.setText(welcome_msg)
        
        return panel
        
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择PDF文件", "", "PDF文件 (*.pdf)"
        )
        if file_path:
            self.on_file_dropped(file_path)
        
    def on_file_dropped(self, file_path):
        if os.path.exists(file_path):
            self.current_file = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"📄 已选择: {file_name}\n📍 路径: {file_path}")
            self.output_dir = os.path.dirname(file_path)
            self.status_display.append(f"\n✅ 已选择文件: {file_name}")
        else:
            self.show_error("文件不存在！")
        
    def run_function(self, function, *args, **kwargs):
        if self.worker_thread and self.worker_thread.isRunning():
            self.show_error("请等待当前操作完成！")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        self.worker_thread = WorkerThread(function, *args, **kwargs)
        self.worker_thread.finished.connect(self.on_function_finished)
        self.worker_thread.error.connect(self.on_function_error)
        self.worker_thread.start()
        
    def on_function_finished(self, result):
        self.progress_bar.setVisible(False)
        self.status_display.append(f"✅ {result}")
        
    def on_function_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.show_error(f"操作失败: {error_msg}")
        
    def show_error(self, message):
        self.status_display.append(f"❌ {message}")
        
    def split_pdf(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在执行PDF拆分...")
        self.run_function(split_pdf, self.current_file, self.output_dir)
        
    def merge_pdf(self):
        self.status_display.append("\n🔧 正在执行PDF合并...")
        files, _ = QFileDialog.getOpenFileNames(self, "选择要合并的PDF文件", "", "PDF文件 (*.pdf)")
        if files:
            output_path = os.path.join(os.path.dirname(files[0]), "merged.pdf")
            self.run_function(merge_pdfs, files, output_path)
        
    def pdf_to_image(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在将PDF转换为图片...")
        self.run_function(pdf_to_images, self.current_file, self.output_dir)
        
    def extract_images(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在从PDF中提取图片...")
        self.run_function(extract_images_from_pdf, self.current_file, self.output_dir)
        
    def extract_tables(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在从PDF中提取表格...")
        self.run_function(extract_tables_from_pdf, self.current_file, self.output_dir)
        
    def extract_text(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在从PDF中提取文本...")
        self.run_function(extract_text_from_pdf, self.current_file, self.output_dir)
        
    def images_to_pdf(self):
        self.status_display.append("\n🔧 正在将图片导入为PDF...")
        files, _ = QFileDialog.getOpenFileNames(self, "选择图片文件", "", 
                                              "图片文件 (*.png *.jpg *.jpeg *.bmp *.tiff)")
        if files:
            output_path = os.path.join(os.path.dirname(files[0]), "images_to_pdf.pdf")
            self.run_function(images_to_pdf, files, output_path)
        
    def batch_print(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在执行批量打印...")
        self.run_function(batch_print_pdfs, [self.current_file])
        
    def protect_pdf(self):
        if not self.check_file_selected():
            return
        
        # 弹出密码输入对话框
        password, ok = QInputDialog.getText(
            self, "设置PDF密码", "请输入PDF保护密码:", 
            echo=QLineEdit.Password  # 使用密码输入模式
        )
        
        # 检查用户是否输入了密码
        if ok and password:
            # 再次输入密码进行确认
            confirm_password, confirm_ok = QInputDialog.getText(
                self, "确认密码", "请再次输入密码进行确认:", 
                echo=QLineEdit.Password
            )
            
            if confirm_ok and confirm_password == password:
                self.status_display.append("\n🔧 正在为PDF添加保护...")
                self.run_function(protect_pdf, self.current_file, self.output_dir, password)
            elif not confirm_ok:
                # 用户取消了确认
                self.status_display.append("❌ PDF保护操作已取消")
            else:
                # 密码不匹配
                self.show_error("两次输入的密码不匹配，请重新尝试！")
        elif not ok:
            # 用户取消了输入
            self.status_display.append("❌ PDF保护操作已取消")
        else:
            # 密码为空
            self.show_error("密码不能为空，请输入有效密码！")
        
    def preview_pdf(self):
        if not self.check_file_selected():
            return
        self.status_display.append("\n🔧 正在预览PDF...")
        self.run_function(preview_pdf, self.current_file)
        
    def check_file_selected(self):
        if not self.current_file:
            self.show_error("请先选择一个PDF文件！")
            return False
        return True

    def closeEvent(self, event):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()
        event.accept()
