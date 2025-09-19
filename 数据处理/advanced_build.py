import os
import subprocess
import sys
from pathlib import Path

def install_packages():
    """安装必要的包"""
    packages = [
        'pyinstaller',
        'pandas',
        'openpyxl', 
        'requests',
        'tkcalendar',
        'schedule'
    ]
    
    for package in packages:
        try:
            __import__(package.split('==')[0])
        except ImportError:
            print(f"正在安装 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def build_executable():
    """构建可执行文件"""
    python_file = "hqmsmjz_time.py"
    
    if not Path(python_file).exists():
        print(f"❌ 文件 {python_file} 不存在")
        # 查找其他可能的文件名
        py_files = list(Path('.').glob('*.py'))
        if py_files:
            print("找到以下Python文件:")
            for file in py_files:
                print(f"  - {file.name}")
            # 使用第一个找到的Python文件
            python_file = py_files[0].name
            print(f"将使用文件: {python_file}")
        else:
            print("❌ 未找到任何Python文件")
            return False
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', '数据导出工具',
        '--hidden-import', 'pandas',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'requests',
        '--hidden-import', 'tkinter',
        '--hidden-import', 'tkcalendar',
        '--hidden-import', 'schedule',
        '--hidden-import', 'dateutil.relativedelta',
        '--hidden-import', 'logging',
        '--clean',
        python_file
    ]
    
    # 如果有图标文件，添加图标参数
    if Path('icon.ico').exists():
        cmd.extend(['--icon', 'icon.ico'])
    
    print("开始打包...")
    print("执行命令:", " ".join(cmd))
    print("-" * 50)
    
    # 使用Popen实时输出日志
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
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
            print(output.strip())
    
    # 获取返回码
    return_code = process.poll()
    
    if return_code == 0:
        print("✅ PyInstaller过程完成！")
        return True
    else:
        print("❌ PyInstaller过程失败！")
        return False

if __name__ == '__main__':
    install_packages()
    success = build_executable()
    
    if success:
        # 显示结果
        dist_path = Path('dist') / '数据导出工具.exe'
        if dist_path.exists():
            print(f"\n✅ 打包成功！")
            print(f"可执行文件位置: {dist_path.absolute()}")
            print(f"文件大小: {dist_path.stat().st_size / (1024 * 1024):.2f} MB")
        else:
            print("\n⚠️  PyInstaller过程完成但未找到可执行文件")
            print("检查dist目录内容:")
            dist_dir = Path('dist')
            if dist_dir.exists():
                for item in dist_dir.iterdir():
                    print(f"  - {item.name}")
            
            # 检查build目录中的.spec文件
            build_dir = Path('build')
            if build_dir.exists():
                spec_files = list(build_dir.glob('*.spec'))
                if spec_files:
                    print("\n找到.spec文件，尝试直接使用pyinstaller构建:")
                    spec_file = spec_files[0]
                    direct_cmd = ['pyinstaller', '--clean', str(spec_file)]
                    print("执行命令:", " ".join(direct_cmd))
                    subprocess.run(direct_cmd)
                    
                    # 再次检查是否生成可执行文件
                    if dist_path.exists():
                        print(f"\n✅ 最终打包成功！")
                        print(f"可执行文件位置: {dist_path.absolute()}")
                    else:
                        print("\n❌ 仍然无法生成可执行文件")
    else:
        print("\n❌ 打包失败！")