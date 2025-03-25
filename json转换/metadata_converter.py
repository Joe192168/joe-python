import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import sys

# 兼容Python 3.5以下版本
if sys.version_info < (3, 5):
    json.JSONDecodeError = ValueError

def transform_metadata(original_data):
    """数据转换核心逻辑"""
    transformed = {"dimensions": [], "measures": []}
    
    # 处理维度
    for dimension in original_data["dimensions"]:
        dim = {
            "uniqueName": dimension["uniqueName"],
            "name": dimension["name"],
            "caption": dimension["caption"],
            "hierarchies": []
        }
        
        for hierarchy in dimension["hierarchies"]:
            hier = {
                "uniqueName": hierarchy["uniqueName"],
                "name": hierarchy["name"],
                "caption": hierarchy["caption"]
            }
            
            if hierarchy.get("hierarchyFlag", False):
                hier["levels"] = [
                    {
                        "uniqueName": level["uniqueName"],
                        "name": level["name"],
                        "caption": level["caption"]
                    } 
                    for level in hierarchy["levels"]
                ]
                
            dim["hierarchies"].append(hier)
        
        transformed["dimensions"].append(dim)
    
    # 处理指标
    transformed["measures"] = [
        {
            "uniqueName": measure["uniqueName"],
            "name": measure["name"],
            "caption": measure["caption"]
        }
        for measure in original_data["measures"]
    ]
    
    return transformed

class JsonConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("元数据转换工具 v1.1")
        self.setup_ui()
        
    def setup_ui(self):
        """界面布局"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="输入", padding=10)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_text = tk.Text(input_frame, height=15, width=80)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="上传文件", command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空输入", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        # 操作按钮
        ttk.Button(main_frame, text="执行转换", command=self.do_conversion).pack(pady=10)
        
        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="输出", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(output_frame, height=15, width=80)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(output_frame, text="保存结果", command=self.save_output).pack(pady=5)
        
    def load_file(self):
        """加载文件到输入区域"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("错误", f"文件读取失败: {str(e)}")
    
    def clear_input(self):
        """清空输入区域"""
        self.input_text.delete(1.0, tk.END)
    
    def do_conversion(self):
        """执行转换操作"""
        input_content = self.input_text.get(1.0, tk.END).strip()
        if not input_content:
            messagebox.showwarning("警告", "输入内容不能为空")
            return
        
        try:
            original_data = json.loads(input_content)
            transformed = transform_metadata(original_data)
            output = json.dumps(transformed, indent=2, ensure_ascii=False)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        except ValueError as e:
            if hasattr(json, 'JSONDecodeError') and isinstance(e, json.JSONDecodeError):
                messagebox.showerror("错误", "无效的 JSON 格式")
            else:
                messagebox.showerror("错误", f"JSON解析错误: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
    
    def save_output(self):
        """保存输出结果"""
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "输出内容为空")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", "文件保存成功")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonConverterApp(root)
    root.mainloop()