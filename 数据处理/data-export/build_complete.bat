@echo off
chcp 65001 >nul
title 数据导出工具 - 完整打包流程

echo ========================================
echo   数据导出工具 - 完整打包流程
echo ========================================

echo 当前目录: %CD%
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

echo ✓ Python已安装

REM 运行修复版打包脚本
echo 启动修复版打包程序...
python data_export_tool_build_fixed.py

if errorlevel 1 (
    echo.
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包流程完成！
echo ========================================
echo.
pause