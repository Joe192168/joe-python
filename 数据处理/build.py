import os
import subprocess
import sys
from pathlib import Path
import shutil
import tempfile
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def build_executable():
    """构建带有图标的可执行文件"""
    # 获取当前脚本所在的目录
    base_dir = Path(__file__).parent
    
    # 查找主Python文件
    python_file = base_dir / "hqmsmjz_time.py"
    if not python_file.exists():
        logging.error(f"文件 {python_file} 不存在")
        return False
    
    # 查找图标文件
    icon_file = base_dir / "icon.ico"
    if not icon_file.exists():
        logging.error(f"图标文件不存在: {icon_file}")
        return False
    
    # 创建临时目录用于构建
    build_dir = Path(tempfile.mkdtemp(prefix="pyinstaller_build_"))
    logging.info(f"创建临时构建目录: {build_dir}")
    
    # 构建命令
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        '--onefile',
        '--windowed',
        '--name', '数据导出工具',
        '--icon', str(icon_file),
        '--add-data', f'{icon_file};.',  # 嵌入图标文件
        '--collect-all', 'tkcalendar',
        '--collect-all', 'babel',
        '--hidden-import', 'numpy',
        '--hidden-import', 'pandas',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'babel',
        '--hidden-import', 'babel.numbers',
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'scipy',
        '--exclude-module', 'PIL',
        '--exclude-module', 'cryptography',
        '--clean',
        '--noconfirm',
        str(python_file)
    ]
    
    logging.info("开始打包...")
    logging.info("执行命令: " + " ".join(cmd))
    
    # 使用Popen实时输出日志
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    # 实时输出日志
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logging.info(output.strip())
    
    # 获取返回码
    return_code = process.poll()
    
    if return_code == 0:
        logging.info("✅ PyInstaller过程完成！")
        
        # 检查项目目录下的dist文件夹
        project_dist_dir = base_dir / 'dist'
        exe_name = '数据导出工具.exe'
        exe_path = project_dist_dir / exe_name
        
        if exe_path.exists():
            logging.info(f"✅ 打包成功！")
            logging.info(f"可执行文件位置: {exe_path.absolute()}")
            logging.info(f"文件大小: {exe_path.stat().st_size / (1024 * 1024):.2f} MB")
            
            # 清理临时目录
            shutil.rmtree(build_dir)
            
            return True
        else:
            logging.error("❌ 可执行文件未生成")
            return False
    else:
        logging.error("❌ PyInstaller过程失败！")
        return False

if __name__ == '__main__':
    build_executable()