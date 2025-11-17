#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication
from ui import PDFToolbox

def main():
    # 添加当前目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    app = QApplication(sys.argv)
    app.setApplicationName("PDF工具箱")
    app.setApplicationVersion("1.0.0")
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    window = PDFToolbox()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
