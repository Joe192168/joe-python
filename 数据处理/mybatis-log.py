import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import re
import json
import os
import threading

def parse_mybatis_log(log_content):
    lines = log_content.split('\n')
    parsed_sqls = []
    i = 0
    while i < len(lines):
        if 'Preparing: insert into t_system_resources' in lines[i]:
            preparing_match = re.search(r'Preparing: (insert into t_system_resources.*)', lines[i])
            if preparing_match:
                sql = preparing_match.group(1).strip()
                j = i + 1
                parameters = None
                while j < len(lines):
                    if 'Parameters:' in lines[j]:
                        params_match = re.search(r'Parameters: (.*)', lines[j])
                        if params_match:
                            parameters = params_match.group(1).strip()
                            break
                    j += 1
                if parameters:
                    param_str = parameters + ','
                    params = re.findall(r'(.*?)\(([^)]+)\)\s*,', param_str)
                    param_list = []
                    for value, param_type in params:
                        value = value.strip()
                        # Handle JSON parameters
                        if param_type == 'String' and value.startswith('{') and value.endswith('}'):
                            try:
                                # Validate JSON and escape it properly
                                json.loads(value)  # Ensure it's valid JSON
                                value = value.replace("'", "''")
                                param_list.append(f"'{value}'")
                            except json.JSONDecodeError:
                                # If not valid JSON, treat as regular string
                                value = value.replace("'", "''")
                                param_list.append(f"'{value}'")
                        elif param_type == 'String' or param_type == 'Timestamp':
                            value = value.replace("'", "''")
                            param_list.append(f"'{value}'")
                        else:
                            param_list.append(value)
                    placeholders = sql.count('?')
                    if len(param_list) == placeholders:
                        for param in param_list:
                            sql = sql.replace('?', param, 1)
                        parsed_sqls.append(sql + ';')
                i = j if j < len(lines) else i + 1
        i += 1
    return parsed_sqls

class App:
    def __init__(self, master):
        self.master = master
        master.title("MyBatis日志解析器")
        master.geometry("800x600")
        
        self.file_paths = []
        self.output_dir = ""
        
        # Files label and list
        self.files_label = tk.Label(master, text="已选择文件：")
        self.files_label.pack(pady=5)
        
        self.files_list = tk.Listbox(master, height=5)
        self.files_list.pack(fill=tk.X, padx=10)
        
        # Select files button
        self.select_files_btn = tk.Button(master, text="选择日志文件", command=self.select_files)
        self.select_files_btn.pack(pady=5)
        
        # Output dir label and entry
        self.output_label = tk.Label(master, text="输出目录：")
        self.output_label.pack(pady=5)
        
        self.output_entry = tk.Entry(master)
        self.output_entry.pack(fill=tk.X, padx=10)
        
        # Select output dir button
        self.select_output_btn = tk.Button(master, text="选择输出目录", command=self.select_output)
        self.select_output_btn.pack(pady=5)
        
        # Process button
        self.process_btn = tk.Button(master, text="处理文件", command=self.start_processing)
        self.process_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(master, length=400, mode='indeterminate')
        self.progress.pack(pady=5)
        
        # Results text
        self.results_text = scrolledtext.ScrolledText(master, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def select_files(self):
        new_files = filedialog.askopenfilenames(title="选择日志文件", filetypes=[("日志文件", "*.log")])
        if new_files:
            self.file_paths.extend(new_files)
            self.update_files_list()

    def update_files_list(self):
        self.files_list.delete(0, tk.END)
        for file in self.file_paths:
            self.files_list.insert(tk.END, os.path.basename(file))

    def select_output(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir = dir_path
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)

    def start_processing(self):
        if not self.file_paths:
            messagebox.showwarning("警告", "未选择任何文件！")
            return
        if not self.output_dir:
            messagebox.showwarning("警告", "未选择输出目录！")
            return
        
        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.results_text.delete(1.0, tk.END)
        
        threading.Thread(target=self.process_files, daemon=True).start()

    def process_files(self):
        total_parsed = 0
        processed_info = []
        
        for file_path in self.file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            parsed_sqls = parse_mybatis_log(log_content)
            parsed_count = len(parsed_sqls)
            total_parsed += parsed_count
            
            base_name = os.path.basename(file_path)
            if parsed_sqls:
                output_file = os.path.join(self.output_dir, base_name.replace('.log', '_parsed.sql'))
                with open(output_file, 'w', encoding='utf-8') as out:
                    out.write('\n'.join(parsed_sqls))
                processed_info.append(f"{base_name}: {parsed_count} 条SQL语句已保存至 {output_file}")
            else:
                processed_info.append(f"{base_name}: 未找到SQL语句")
        
        self.master.after(0, self.finish_processing, total_parsed, processed_info)

    def finish_processing(self, total_parsed, processed_info):
        self.progress.stop()
        self.process_btn.config(state=tk.NORMAL)
        
        results = "处理完成！\n\n"
        results += f"总计处理文件数：{len(self.file_paths)}\n"
        results += f"总计解析SQL语句数：{total_parsed}\n\n"
        results += "\n".join(processed_info)
        
        self.results_text.insert(tk.END, results)
        
        messagebox.showinfo("完成", "处理完成！")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()