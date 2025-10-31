# fix_tkcalendar_packaging.py
import os
import sys
import subprocess
import shutil
from pathlib import Path

def collect_tkcalendar_files():
    """收集tkcalendar的所有必要文件"""
    try:
        import tkcalendar
        tkcalendar_path = Path(tkcalendar.__file__).parent
        
        # 获取tkcalendar包的所有文件
        tkcalendar_files = []
        for file_path in tkcalendar_path.rglob('*'):
            if file_path.is_file():
                # 计算相对路径
                rel_path = file_path.relative_to(tkcalendar_path.parent)
                tkcalendar_files.append((str(file_path), str(rel_path.parent)))
        
        return tkcalendar_files
    except ImportError as e:
        print(f"无法导入tkcalendar: {e}")
        return []

def create_tkcalendar_spec():
    """创建包含tkcalendar的spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files

block_cipher = None

# 收集各个模块的文件
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')

# 手动添加tkcalendar的数据文件
tkcalendar_datas = []
try:
    import tkcalendar
    tkcalendar_path = os.path.dirname(tkcalendar.__file__)
    for root, dirs, files in os.walk(tkcalendar_path):
        for file in files:
            if file.endswith(('.tcl', '.txt', '.json', '.conf')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, os.path.dirname(tkcalendar_path))
                tkcalendar_datas.append((full_path, os.path.join('tkcalendar', rel_path)))
except ImportError:
    pass

# 合并数据文件
datas = numpy_datas + pandas_datas + tkcalendar_datas
binaries = numpy_binaries + pandas_binaries

# 隐藏导入
hiddenimports = numpy_hiddenimports + pandas_hiddenimports + [
    'tkcalendar',
    'tkcalendar.calendar_',
    'tkcalendar.dateentry',
    'tkcalendar.popup',
    'tkcalendar.tooltip',
    'babel.numbers',
    'babel.core',
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.utils',
    'dateutil',
    'dateutil.relativedelta',
    'dateutil.parser',
    'dateutil.tz',
    'requests',
    'schedule',
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
    excludes=[
        'tkinter.test',
        'matplotlib',
        'scipy',
        'pytest',
        'unittest',
    ],
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
    
    with open('tkcalendar_fixed.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

def build_with_tkcalendar_fix():
    """使用tkcalendar修复进行构建"""
    print("使用tkcalendar修复进行打包...")
    
    # 创建spec文件
    create_tkcalendar_spec()
    
    # 清理构建目录
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 使用新的spec文件打包
    cmd = [sys.executable, '-m', 'PyInstaller', 'tkcalendar_fixed.spec', '--clean']
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        print("✓ 打包成功！")
        return True
    else:
        print("✗ 打包失败")
        print(result.stderr)
        return False

if __name__ == "__main__":
    build_with_tkcalendar_fix()