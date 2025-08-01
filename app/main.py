
import os
import sys
import subprocess
import platform
import webbrowser
import tkinter as tk
import importlib.util  # 确保已添加此导入
from tkinter import ttk, filedialog, messagebox, scrolledtext
# 获取基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUNCTION_DIR = os.path.join(BASE_DIR, 'function')

# 确保FUNCTION_DIR使用正确的路径分隔符
FUNCTION_DIR = os.path.normpath(FUNCTION_DIR)

# 将function目录添加到Python路径（使用绝对路径）
if FUNCTION_DIR not in sys.path:
    sys.path.append(FUNCTION_DIR)
    # 删除路径添加提示
    # print(f"Added {FUNCTION_DIR} to sys.path")


SCRIPT_DIR = os.path.join(BASE_DIR, 'script')
DOCUMENT_DIR = os.path.join(BASE_DIR, 'document')


if FUNCTION_DIR not in sys.path:
    sys.path.append(FUNCTION_DIR)
    # print(f"Added {FUNCTION_DIR} to sys.path")

OutputManager = None
output_manager_path = os.path.join(FUNCTION_DIR, 'base', 'output_manager.py')
# 可选：删除动态导入的信息输出
if os.path.exists(output_manager_path):
    # 删除动态导入提示
    # print(f"Dynamically importing {output_manager_path}")
    try:
        # 创建模块规范
        spec = importlib.util.spec_from_file_location('function.base.output_manager', output_manager_path)
        # 创建模块对象
        output_manager_module = importlib.util.module_from_spec(spec)
        # 执行模块加载
        spec.loader.exec_module(output_manager_module)
        # 获取OutputManager类
        OutputManager = output_manager_module.OutputManager
        # 删除成功提示
        # print("Successfully dynamically imported OutputManager")
    except Exception as e:
        # 建议保留错误信息
        print(f"Error dynamically importing output_manager.py: {e}")
else:
    print(f"output_manager.py does not exist at {output_manager_path}")


class PythonEnvManager:
    def __init__(self, root):
        self.root = root
        self.root.title("U盘Python环境管理器")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        # 添加程序退出时的回调函数
        def on_closing():
            if self.panel_manager:
                # 保存面板配置
                self.panel_manager.save_panel_config()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        # 添加显示跑码窗口的开关变量
        self.show_update_window = tk.BooleanVar(value=True)
        
        # 存储按钮列表
        self.buttons = []

        # 设置字体 - 先设置字体样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Microsoft YaHei", 12))
        self.style.configure("TLabel", font=("Microsoft YaHei", 12), background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Microsoft YaHei", 16, "bold"), background="#4a7abc", foreground="white")

        # 创建标题栏
        header_frame = ttk.Frame(root, style="Header.TLabel")
        header_frame.pack(fill=tk.X)
        header_label = ttk.Label(header_frame, text="U盘Python环境管理器", style="Header.TLabel")
        header_label.pack(pady=10)

        # 创建功能按钮列表
        button_width = 20
        button_height = 2
        self.buttons = [
            ("更新库", self.update_libraries),
            ("安装新库", self.install_library),
            ("执行Python程序", self.run_python_script),
            ("查看版本", self.check_version),
            ("面板设置", self.open_panel_settings)  # 添加面板设置按钮
        ]

        # 网格布局按钮 - 先初始化button_frame
        self.button_frame = ttk.Frame(root, padding=20)
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # 创建状态栏和输出按钮（只创建一次）
        self.status_frame = ttk.Frame(root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # 添加显示输出按钮
        self.output_frame = ttk.Frame(self.status_frame)
        self.output_frame.pack(side=tk.LEFT, padx=10, pady=5)
        self.output_button = ttk.Button(self.output_frame, text="显示输出")
        self.output_button.pack(side=tk.LEFT)

        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=5)

        # 初始化输出管理器
        self.output_manager = OutputManager(root)
        self.output_manager.initialize(self.output_button, self.status_var)
        self.output_button.config(command=self.output_manager.toggle_output_window)

        # 先动态导入PanelManager并初始化 - 关键修改
        self.panel_manager = None
        panel_manager_path = os.path.join(FUNCTION_DIR, 'panel_manager.py')
        if os.path.exists(panel_manager_path):
            try:
                spec = importlib.util.spec_from_file_location('function.panel_manager', panel_manager_path)
                panel_manager_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(panel_manager_module)
                self.panel_manager = panel_manager_module.PanelManager(root, self)
            except Exception as e:
                print(f"导入panel_manager.py失败: {e}")

        # 最后调用方法构建按钮面板 - 关键修改
        self.rebuild_button_panel()

    def rebuild_button_panel(self):
        """重建按钮面板"""
        # 清空现有按钮
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # 网格布局按钮
        button_width = 20
        for i, (text, command) in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            btn = ttk.Button(self.button_frame, text=text, command=command,
                             width=button_width, padding=(5, 10))
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
        # 设置网格权重，使按钮能够随窗口大小调整
        for i in range(3):
            self.button_frame.grid_columnconfigure(i, weight=1)
        # 计算需要的行数
        row_count = (len(self.buttons) + 2) // 3
        for i in range(row_count):
            self.button_frame.grid_rowconfigure(i, weight=1)
        # 删除额外的行权重，使按钮顶部对齐
        self.button_frame.grid_rowconfigure(row_count, weight=1)

    def update_status(self, message):
        """更新状态栏消息"""
        self.status_var.set(message)
        self.root.update_idletasks()

    def update_libraries(self):
        """更新库"""
        try:
            # 调用function目录中的update.py脚本
            update_script = os.path.join(FUNCTION_DIR, 'update.py')
            if os.path.exists(update_script):
                # 自动显示输出窗口
                self.output_manager.show_output_window()
                # 运行命令并显示输出
                self.output_manager.run_command_with_output([sys.executable, update_script], "更新库")
            else:
                messagebox.showerror("错误", f"找不到更新脚本：{update_script}")
                self.update_status("更新失败")
        except Exception as e:
            self.update_status("更新失败")
            messagebox.showerror("错误", f"更新过程中出错：{str(e)}")

    def install_library(self):
        """安装新库"""
        # 创建输入对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("安装新库")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
        y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # 添加标签和输入框
        ttk.Label(dialog, text="请输入要安装的库名称：", background="#f0f0f0").pack(pady=20)
        lib_entry = ttk.Entry(dialog, width=30, font=("Microsoft YaHei", 12))
        lib_entry.pack(pady=10)
        lib_entry.focus_set()

        def do_install():
            lib_name = lib_entry.get().strip()
            if not lib_name:
                messagebox.showwarning("警告", "请输入库名称！")
                return

            try:
                # 调用function目录中的install_library.py脚本
                install_script = os.path.join(FUNCTION_DIR, 'install_library.py')
                if os.path.exists(install_script):
                    # 自动显示输出窗口
                    self.output_manager.show_output_window()
                    # 运行命令并显示输出
                    self.output_manager.run_command_with_output([sys.executable, install_script, lib_name], f"安装库 {lib_name}")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", f"找不到安装脚本：{install_script}")
                    self.update_status("安装失败")
            except Exception as e:
                self.update_status("安装失败")
                messagebox.showerror("错误", f"安装库时出错：{str(e)}")

        # 添加按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="安装", command=do_install).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def run_python_script(self):
        """执行Python程序"""
        self.update_status("正在打开文件选择对话框...")
        try:
            # 确保script目录存在
            if not os.path.exists(SCRIPT_DIR):
                os.makedirs(SCRIPT_DIR)
                messagebox.showinfo("提示", "script文件夹已创建，请将Python程序放入该文件夹后重试。")
                self.update_status("就绪")
                return

            # 打开文件选择对话框
            file_path = filedialog.askopenfilename(
                title="选择Python程序",
                initialdir=SCRIPT_DIR,
                filetypes=[("Python Files", "*.py")]
            )

            if file_path:
                self.update_status(f"正在执行：{os.path.basename(file_path)}...")
                try:
                    # 执行Python脚本
                    subprocess.Popen([sys.executable, file_path])
                    self.update_status("程序执行中")
                except Exception as e:
                    self.update_status("程序执行失败")
                    messagebox.showerror("错误", f"执行程序时出错：{str(e)}")
            else:
                self.update_status("已取消选择")
        except Exception as e:
            self.update_status("打开文件选择对话框失败")
            messagebox.showerror("错误", f"打开文件选择对话框时出错：{str(e)}")

    def check_version(self):
        """查看版本"""
        self.update_status("正在获取版本信息...")
        try:
            # 调用function目录中的check_version.py脚本
            version_script = os.path.join(FUNCTION_DIR, 'check_version.py')
            if os.path.exists(version_script):
                # 自动显示输出窗口
                self.output_manager.show_output_window()
                # 运行命令并显示输出
                self.output_manager.run_command_with_output([sys.executable, version_script], "查看版本信息")
            else:
                messagebox.showerror("错误", f"找不到版本信息脚本：{version_script}")
                self.update_status("获取版本信息失败")
        except Exception as e:
            self.update_status("获取版本信息失败")
            messagebox.showerror("错误", f"获取版本信息时出错：{str(e)}")

    def open_panel_settings(self):
        """打开面板设置"""
        if self.panel_manager:
            self.panel_manager.panel_settings()
        else:
            messagebox.showerror("错误", "面板管理器加载失败")




if __name__ == "__main__":
    root = tk.Tk()
    app = PythonEnvManager(root)
    root.mainloop()
