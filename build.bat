@echo off
chcp 65001
title PDF工具箱打包程序

echo ========================================
echo          PDF工具箱打包程序
echo ========================================
echo.

echo 1. 检查依赖包安装...
pip install -r requirements.txt

echo.
echo 2. 开始打包...
pyinstaller pdf_toolbox.spec

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo           打包成功！
    echo ========================================
    echo 可执行文件位置: dist\PDF工具箱.exe
    echo.
    echo 请将 README.txt 与可执行文件一起分发
    echo.
) else (
    echo.
    echo ========================================
    echo           打包失败！
    echo ========================================
    echo 请检查错误信息
)

echo.
pause
