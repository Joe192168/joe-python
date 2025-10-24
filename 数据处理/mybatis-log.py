import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import json
import os
import threading

class LogProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("日志文件处理工具")
        self.root.geometry("600x400")

        self.file_paths = []
        self.output_dir = ""

        # 选择日志文件按钮
        self.select_files_btn = tk.Button(root, text="选择日志文件（可批量）", command=self.select_files)
        self.select_files_btn.pack(pady=10)

        # 显示选择的日志文件
        self.files_label = tk.Label(root, text="选择的日志文件：无")
        self.files_label.pack(pady=5)

        # 选择存储目录按钮
        self.select_dir_btn = tk.Button(root, text="选择存储目录", command=self.select_directory)
        self.select_dir_btn.pack(pady=10)

        # 显示选择的存储目录
        self.dir_label = tk.Label(root, text="存储目录：无")
        self.dir_label.pack(pady=5)

        # 开始处理按钮
        self.process_btn = tk.Button(root, text="开始处理", command=self.start_processing)
        self.process_btn.pack(pady=10)

        # 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # 状态标签
        self.status_label = tk.Label(root, text="状态：就绪")
        self.status_label.pack(pady=5)

        # 匹配情况标签
        self.match_label = tk.Label(root, text="匹配情况：")
        self.match_label.pack(pady=5)

    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="选择日志文件",
            filetypes=[("Log files", "*.log"), ("All files", "*.*")]
        )
        if self.file_paths:
            self.files_label.config(text=f"选择的日志文件：{len(self.file_paths)} 个")

    def select_directory(self):
        self.output_dir = filedialog.askdirectory(title="选择存储目录")
        if self.output_dir:
            self.dir_label.config(text=f"存储目录：{self.output_dir}")

    def start_processing(self):
        if not self.file_paths:
            messagebox.showerror("错误", "请先选择日志文件")
            return
        if not self.output_dir:
            messagebox.showerror("错误", "请先选择存储目录")
            return

        # 禁用按钮防止重复点击
        self.process_btn.config(state=tk.DISABLED)
        self.status_label.config(text="状态：处理中...")

        # 使用线程运行处理函数，避免阻塞GUI
        threading.Thread(target=self.process_files).start()

    def process_files(self):
        total_files = len(self.file_paths)
        self.progress["maximum"] = total_files
        total_matches = 0

        for idx, file_path in enumerate(self.file_paths):
            matches = self.process_log_file(file_path)
            total_matches += matches
            self.progress["value"] = idx + 1
            self.root.update_idletasks()  # 更新GUI

        self.status_label.config(text="状态：处理完成")
        self.match_label.config(text=f"匹配情况：总共匹配到 {total_matches} 条 insert into t_system_resources 语句")
        self.process_btn.config(state=tk.NORMAL)
        messagebox.showinfo("完成", "处理完成！")

    def process_log_file(self, file_path):
        output_file = os.path.join(self.output_dir, f"processed_{os.path.basename(file_path)}")
        match_count = 0
        with open(file_path, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out_f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                # 查找 Preparing 行
                if '==>  Preparing: ' in line:
                    sql_match = re.search(r'==>  Preparing: (.*)$', line)
                    if sql_match:
                        sql = sql_match.group(1).strip()
                        if sql.startswith('insert into t_system_resources') or sql.startswith('update t_system_resources'):
                            # 查找下一行的 Parameters
                            if i + 1 < len(lines) and '==> Parameters: ' in lines[i + 1]:
                                params = self.parse_parameters(lines[i + 1].strip())
                                # 替换 SQL 中的占位符
                                final_sql = self.replace_sql_placeholders(sql, params)
                                out_f.write(final_sql + ';\n')
                                match_count += 1
                        i += 2  # 跳过 Parameters 行
                        continue
                i += 1
        return match_count

    def parse_parameters(self, param_line):
        """解析 Parameters 行，处理 JSON 和其他类型的参数"""
        # 提取 Parameters 后的内容
        param_match = re.search(r'==> Parameters: (.*)$', param_line)
        if not param_match:
            return []
        
        param_str = param_match.group(1)
        params = []
        current_param = ""
        brace_count = 0
        in_json = False
        i = 0

        while i < len(param_str):
            char = param_str[i]
            
            if char == '{':
                brace_count += 1
                in_json = True
                current_param += char
            elif char == '}':
                brace_count -= 1
                current_param += char
                if brace_count == 0:
                    in_json = False
            elif char == ',' and brace_count == 0 and not in_json:
                # 遇到逗号且不在 JSON 内部，分割参数
                stripped_param = current_param.strip()
                param_type_match = re.match(r'^(.*)\((.*?)\)$', stripped_param)
                if param_type_match:
                    value, param_type = param_type_match.groups()
                    params.append((value.strip(), param_type.strip()))
                elif stripped_param.lower() == "null":
                    params.append(("null", "null"))
                current_param = ""
                i += 1
                continue
            else:
                current_param += char
            i += 1

        # 处理最后一个参数
        stripped_param = current_param.strip()
        if stripped_param:
            param_type_match = re.match(r'^(.*)\((.*?)\)$', stripped_param)
            if param_type_match:
                value, param_type = param_type_match.groups()
                params.append((value.strip(), param_type.strip()))
            elif stripped_param.lower() == "null":
                params.append(("null", "null"))

        # 处理 JSON 参数
        processed_params = []
        for value, param_type in params:
            if param_type == "null":
                processed_params.append("NULL")
            elif param_type == 'String':
                # 转义单引号
                escaped_value = value.replace("'", "''")
                if value.startswith('{') and value.endswith('}'):
                    try:
                        # 尝试解析 JSON 以验证
                        json.loads(value)
                        processed_params.append(f"'{escaped_value}'")
                    except json.JSONDecodeError:
                        processed_params.append(f"'{escaped_value}'")
                else:
                    processed_params.append(f"'{escaped_value}'")
            elif param_type == 'Timestamp':
                processed_params.append(f"'{value}'")
            elif param_type in ('BigDecimal', 'Long', 'Integer'):
                processed_params.append(value)
            else:
                processed_params.append(value)
        
        return processed_params

    def replace_sql_placeholders(self, sql, params):
        """将参数替换到 SQL 语句中的占位符"""
        for param in params:
            sql = sql.replace('?', param, 1)
        return sql

if __name__ == "__main__":
    root = tk.Tk()
    app = LogProcessorApp(root)
    root.mainloop()