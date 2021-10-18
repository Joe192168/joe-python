# joe-python

1、爬虫jd时，需要安装谷歌驱动
https://www.cnblogs.com/blogwangwang/p/9608131.html
2、python打包命令
pyinstaller -c -F --icon=my.ico yp.py

pyinstaller 常用命令参数

-F, --onefile Py代码只有一个文件
-D, --onedir Py代码放在一个目录中（默认是这个）
-K, --tk 包含TCL/TK
-d, --debug 生成debug模式的exe文件
-w, --windowed, --noconsole 窗体exe文件(Windows Only)
-c, --nowindowed, --console 控制台exe文件(Windows Only)
-X, --upx 使用upx压缩exe文件
-o DIR, --out=DIR 设置spec文件输出的目录，默认在PyInstaller同目录
--icon=FILE.ICO  加入图标（Windows Only）
-v FILE, --version=FILE 加入版本信息文件

3、key打包加密组件安装

pip install pycrypto
手动下载网址
https://www.dlitz.net/software/pycrypto/

4、ai智能抠图网址
https://www.remove.bg/
http://ai.baidu.com/tech/body/seg

5、OpenCV-Python教程
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html

6、解决FileNotFoundError: [Errno 2] No such file or directory:'C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\1\\_MEI54762\\jieba\\dict.txt'问题
上面就是没把python库jieba的dict.txt打包进来，导致了错误 那么，解决问题也很简单，自己写个hook，然后放进pyinstaller的hooks里面即可
hook文件的命名规范为: hook-【库名】.py，以结巴分词为例，即为hook-jieba.py，然后简单敲入以下两行：

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("jieba")

接下来，找到pyinstaller的hooks文件夹，大概位于：

python根目录\Lib\site-packages\PyInstaller\hooks下，然后把hook-jieba.py丢进去

打包 pyinstaller -F --icon=favicon.ico matching.py


7、qrcode-url

pip install image

pip install qrcode

pip install pillow 