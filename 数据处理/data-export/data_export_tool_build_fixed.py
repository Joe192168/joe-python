#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_environment():
    """检查环境"""
    print("=" * 60)
    print("数据导出工具 - 修复版打包程序")
    print("=" * 60)
    
    # 检查Python
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        print(f"Python版本: {result.stdout.strip()}")
    except:
        print("错误: 无法获取Python版本")
        return False
    
    return True

def install_dependencies():
    """安装依赖"""
    print("\n1. 安装必要的依赖包...")
    
    packages = [
        'numpy==1.24.3',  # 固定版本，避免兼容性问题
        'pandas==2.0.3',
        'requests==2.31.0',
        'openpyxl==3.1.2',
        'tkcalendar==1.6.1',
        'python-dateutil==2.8.2',
        'schedule==1.2.0',
        'pyinstaller==5.13.0'
    ]
    
    for package in packages:
        try:
            # 尝试导入包
            package_name = package.split('==')[0]
            __import__(package_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"正在安装 {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"✗ {package} 安装失败，尝试安装最新版...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

def create_numpy_fixed_spec():
    """创建修复numpy问题的spec文件"""
    print("\n2. 创建修复版spec文件...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# 强制包含numpy的所有文件
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')

# 合并数据文件和二进制文件
datas = numpy_datas + pandas_datas
binaries = numpy_binaries + pandas_binaries

# 隐藏导入
hiddenimports = numpy_hiddenimports + pandas_hiddenimports + [
    'tkcalendar',
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.utils',
    'dateutil',
    'dateutil.relativedelta',
    'requests',
    'schedule',
    'logging.handlers',
]

# 排除的模块
excludes = [
    'tkinter.test',
    'matplotlib',
    'scipy',
    'pytest',
    'unittest',
]

a = Analysis(
    ['data_export_tool.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='数据导出工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codepage='utf-8',
)
'''
    
    with open('numpy_fixed.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ 已创建numpy修复版spec文件: numpy_fixed.spec")

def clean_build_dirs():
    """清理构建目录"""
    print("\n3. 清理构建目录...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 已清理 {dir_name} 目录")

def build_with_spec():
    """使用spec文件打包"""
    print("\n4. 开始打包...")
    
    # 使用spec文件打包
    cmd = [sys.executable, '-m', 'PyInstaller', 'numpy_fixed.spec', '--clean']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            # 检查生成的文件
            exe_path = Path('dist') / '数据导出工具.exe'
            if exe_path.exists():
                file_size = exe_path.stat().st_size / 1024 / 1024
                print(f"✓ 打包成功: {exe_path}")
                print(f"✓ 文件大小: {file_size:.2f} MB")
                return True
            else:
                print("✗ EXE文件未生成")
                return False
        else:
            print("✗ 打包失败")
            if result.stderr:
                print("错误输出:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ 打包过程中出错: {e}")
        return False

def test_exe():
    """测试生成的EXE文件"""
    print("\n5. 测试EXE文件...")
    
    exe_path = Path('dist') / '数据导出工具.exe'
    if not exe_path.exists():
        print("✗ EXE文件不存在，无法测试")
        return False
    
    # 创建一个简单的测试脚本
    test_script = '''
import subprocess
import time
import os

exe_path = os.path.join('dist', '数据导出工具.exe')
if os.path.exists(exe_path):
    try:
        # 启动EXE并等待几秒后关闭
        process = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # 等待5秒
        process.terminate()  # 正常终止
        process.wait(timeout=3)
        print("✓ EXE文件可以启动")
    except Exception as e:
        print(f"✗ EXE文件测试失败: {e}")
else:
    print("✗ EXE文件不存在")
'''
    
    with open('test_exe.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    try:
        result = subprocess.run([sys.executable, 'test_exe.py'], capture_output=True, text=True, timeout=10)
        print(result.stdout)
        if "可以启动" in result.stdout:
            return True
    except:
        print("ℹ 无法自动测试EXE文件，请手动测试")
    
    # 清理测试文件
    if os.path.exists('test_exe.py'):
        os.remove('test_exe.py')
    
    return True  # 即使测试失败也不影响打包结果

def main():
    """主函数"""
    if not check_environment():
        return
    
    try:
        # 安装依赖
        install_dependencies()
        
        # 创建spec文件
        create_numpy_fixed_spec()
        
        # 清理目录
        clean_build_dirs()
        
        # 打包
        if build_with_spec():
            # 测试EXE文件
            test_exe()
            
            print("\n" + "=" * 60)
            print("打包完成！")
            print("EXE文件位置: dist\\数据导出工具.exe")
            print("请双击运行测试功能是否正常")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("打包失败，请检查错误信息")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n✗ 程序执行过程中出错: {e}")
        print("=" * 60)

if __name__ == "__main__":
    main()