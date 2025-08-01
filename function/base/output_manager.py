import os
import sys
import subprocess
import platform
import tkinter as tk
import json  # 添加json模块导入
from tkinter import ttk, scrolledtext, messagebox

class OutputManager:
    def __init__(self, root):
        self.root = root
        self.output_window = None
        self.output_window_visible = False
        self.common_commands = {}
        self.keep_input_var = None
        self.command_input = None
        self.cmd_menu = None
        self.cmd_menu_var = None
        self.output_button = None
        self.status_var = None

    def initialize(self, output_button, status_var):
        """初始化输出管理器"""
        self.output_button = output_button
        self.status_var = status_var
        self.load_common_commands()

    def toggle_output_window(self):
        """切换输出窗口的显示/隐藏状态"""
        if self.output_window_visible:
            self.hide_output_window()
        else:
            self.show_output_window()

    def hide_output_window(self):
        """隐藏输出窗口"""
        if self.output_window and self.output_window.winfo_exists():
            self.output_window.withdraw()
            self.output_window_visible = False
            self.output_button.config(text="显示输出")

    def show_output_window(self):
        """显示命令输出窗口"""
        # 如果窗口已存在且未关闭，则直接显示
        if self.output_window and self.output_window.winfo_exists():
            self.output_window.deiconify()
            self.output_window_visible = True
            self.output_button.config(text="隐藏输出")
            # 如果有正在运行的进程，重新启动输出更新
            if self.current_process and self.current_process.poll() is None:
                self.update_output(self.current_process, "更新库")
            return

        self.output_window = tk.Toplevel(self.root)
        self.output_window.title("命令输出")
        self.output_window.geometry("700x400")
        self.output_window.minsize(500, 300)
        self.output_window.resizable(True, True)
        self.output_window.transient(self.root)
        # 拦截窗口关闭事件，改为隐藏窗口
        self.output_window.protocol("WM_DELETE_WINDOW", self.hide_output_window)

        self.output_window_visible = True
        self.output_button.config(text="隐藏输出")

        # 使用grid布局
        self.output_window.grid_rowconfigure(1, weight=1)  # 文本框区域可扩展
        self.output_window.grid_columnconfigure(0, weight=1)

        # 添加顶部按钮框架
        btn_frame = ttk.Frame(self.output_window)
        btn_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # 使用grid布局管理按钮
        btn_frame.grid_columnconfigure(0, weight=1)  # 左侧区域
        btn_frame.grid_columnconfigure(1, weight=0)  # 分隔符
        btn_frame.grid_columnconfigure(2, weight=0)  # 常用命令区域

        # 左侧按钮区域
        left_btn_frame = ttk.Frame(btn_frame)
        left_btn_frame.grid(row=0, column=0, sticky="w")

        # 添加停止按钮
        ttk.Button(left_btn_frame, text="停止", command=self.stop_command).pack(side=tk.LEFT, padx=(0, 5))

        # 添加清除输出按钮
        ttk.Button(left_btn_frame, text="清除输出", command=self.clear_output).pack(side=tk.LEFT, padx=(0, 5))

        # 添加分隔符
        ttk.Separator(btn_frame, orient=tk.VERTICAL).grid(row=0, column=1, sticky="ns", padx=5)

        # 常用命令区域
        cmd_frame = ttk.Frame(btn_frame)
        cmd_frame.grid(row=0, column=2, sticky="w")

        # 添加常用命令下拉菜单
        self.cmd_menu_var = tk.StringVar(value="选择常用命令...")
        self.cmd_menu = ttk.Combobox(cmd_frame, textvariable=self.cmd_menu_var, values=list(self.common_commands.keys()), width=15, state="readonly")
        self.cmd_menu.pack(side=tk.LEFT, padx=(0, 5))
        self.cmd_menu.bind("<<ComboboxSelected>>", self.on_command_select)
        # 修复：创建完cmd_menu后立即加载常用命令
        self.load_common_commands()

        # 删除有问题的鼠标点击事件绑定
        # self.cmd_menu.bind("<Button-1>", lambda e: self.cmd_menu.event_generate("<<ComboboxSelected>>") if self.cmd_menu.get() != "选择常用命令..." else None)

        # 添加配置按钮
        ttk.Button(cmd_frame, text="配置", command=self.configure_common_commands).pack(side=tk.LEFT)

        # 添加滚动文本框显示输出
        self.output_text = scrolledtext.ScrolledText(self.output_window, wrap=tk.WORD, font=("Microsoft YaHei", 10))
        self.output_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.output_text.config(state=tk.DISABLED)

        # 添加保留输入框内容的变量
        self.keep_input_var = tk.BooleanVar(value=True)  # 默认选中保留

        # 添加命令输入框和执行按钮
        input_frame = ttk.Frame(self.output_window)
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        input_frame.grid_columnconfigure(1, weight=1)  # 修改为列1可扩展

        # 添加复选框 - 控制是否保留输入内容
        ttk.Checkbutton(input_frame, text="保留命令", variable=self.keep_input_var).grid(row=0, column=0, padx=(0, 10))

        self.command_input = ttk.Entry(input_frame, font=("Microsoft YaHei", 10))
        self.command_input.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.command_input.bind("<Return>", lambda event: self.execute_command())

        ttk.Button(input_frame, text="执行", command=self.execute_command).grid(row=0, column=2)

        # 确保输入框获得焦点
        self.command_input.focus_set()

    def load_common_commands(self):
        cmd_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "common_commands.json")
        
        if os.path.exists(cmd_file):
            try:
                with open(cmd_file, 'r', encoding='utf-8') as f:
                    self.common_commands = json.load(f)
                # 检查cmd_menu是否已经创建
                if self.cmd_menu is not None:
                    self.cmd_menu['values'] = list(self.common_commands.keys())
            except Exception as e:
                self.run_command_with_output("", f"加载常用命令失败: {str(e)}")
        else:
            self.run_command_with_output("", f"常用命令文件不存在: {cmd_file}")

    def save_common_commands(self):
        # 修改前的路径
        # cmd_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "common_commands.json")
        
        # 修改后的路径
        cmd_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "common_commands.json")
        
        try:
            with open(cmd_file, 'w', encoding='utf-8') as f:
                json.dump(self.common_commands, f, ensure_ascii=False, indent=4)
            self.update_output(None, "常用命令已保存")  # 添加 None 作为 process 参数
        except Exception as e:
            self.update_output(None, f"保存常用命令失败: {str(e)}")  # 添加 None 作为 process 参数

    def configure_common_commands(self):
        """打开常用命令配置对话框"""
        # 创建配置窗口
        config_window = tk.Toplevel(self.root)
        config_window.title("配置常用命令")
        config_window.geometry("500x300")
        config_window.resizable(True, True)
        config_window.transient(self.root)

        # 添加列表框显示当前命令
        frame_list = ttk.Frame(config_window)
        frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame_list, text="常用命令列表:").pack(anchor=tk.W)

        cmd_listbox = tk.Listbox(frame_list, width=50, height=10)
        cmd_listbox.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        # 滚动条
        scrollbar = ttk.Scrollbar(cmd_listbox, orient=tk.VERTICAL, command=cmd_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        cmd_listbox.config(yscrollcommand=scrollbar.set)

        # 更新列表框内容
        def update_cmd_listbox():
            cmd_listbox.delete(0, tk.END)
            for name, cmd in self.common_commands.items():
                cmd_listbox.insert(tk.END, f"{name}: {cmd}")

        update_cmd_listbox()

        # 添加操作按钮
        frame_buttons = ttk.Frame(config_window)
        frame_buttons.pack(fill=tk.X, padx=10, pady=(0, 10))

        def add_common_command():
            """添加常用命令"""
            # 创建添加对话框
            add_window = tk.Toplevel(self.root)
            add_window.title("添加常用命令")
            add_window.geometry("300x150")
            add_window.resizable(False, False)
            add_window.transient(self.root)

            # 添加表单
            ttk.Label(add_window, text="命令名称:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
            name_entry = ttk.Entry(add_window, width=20)
            name_entry.grid(row=0, column=1, padx=10, pady=10)

            ttk.Label(add_window, text="命令内容:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
            cmd_entry = ttk.Entry(add_window, width=20)
            cmd_entry.grid(row=1, column=1, padx=10, pady=10)

            # 确定按钮
            def do_add():
                name = name_entry.get().strip()
                cmd = cmd_entry.get().strip()
                if name and cmd:
                    self.common_commands[name] = cmd
                    self.save_common_commands()
                    update_cmd_listbox()
                    # 更新下拉菜单
                    self.cmd_menu['values'] = list(self.common_commands.keys())
                    add_window.destroy()
                else:
                    messagebox.showerror("错误", "命令名称和内容都不能为空!")

            ttk.Button(add_window, text="确定", command=do_add).grid(row=2, column=0, columnspan=2, pady=10)

        def edit_common_command():
            """修改常用命令"""
            selection = cmd_listbox.curselection()
            if not selection:
                messagebox.showinfo("提示", "请先选择要修改的命令!")
                return

            selected_item = cmd_listbox.get(selection[0])
            # 解析名称和命令
            if ': ' in selected_item:
                name, cmd = selected_item.split(': ', 1)

                # 创建修改对话框
                edit_window = tk.Toplevel(self.root)
                edit_window.title("修改常用命令")
                edit_window.geometry("300x150")
                edit_window.resizable(False, False)
                edit_window.transient(self.root)

                # 添加表单
                ttk.Label(edit_window, text="命令名称:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
                name_entry = ttk.Entry(edit_window, width=20)
                name_entry.grid(row=0, column=1, padx=10, pady=10)
                name_entry.insert(0, name)

                ttk.Label(edit_window, text="命令内容:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
                cmd_entry = ttk.Entry(edit_window, width=20)
                cmd_entry.grid(row=1, column=1, padx=10, pady=10)
                cmd_entry.insert(0, cmd)

                # 确定按钮
                def do_edit():
                    new_name = name_entry.get().strip()
                    new_cmd = cmd_entry.get().strip()
                    if new_name and new_cmd:
                        # 删除旧命令
                        del self.common_commands[name]
                        # 添加新命令
                        self.common_commands[new_name] = new_cmd
                        self.save_common_commands()
                        update_cmd_listbox()
                        # 更新下拉菜单
                        self.cmd_menu['values'] = list(self.common_commands.keys())
                        edit_window.destroy()
                    else:
                        messagebox.showerror("错误", "命令名称和内容都不能为空!")

                ttk.Button(edit_window, text="确定", command=do_edit).grid(row=2, column=0, columnspan=2, pady=10)

        def delete_common_command():
            """删除常用命令"""
            selection = cmd_listbox.curselection()
            if not selection:
                messagebox.showinfo("提示", "请先选择要删除的命令!")
                return

            selected_item = cmd_listbox.get(selection[0])
            # 解析名称
            if ': ' in selected_item:
                name = selected_item.split(': ', 1)[0]

                if messagebox.askyesno("确认", f"确定要删除命令 '{name}' 吗?"):
                    del self.common_commands[name]
                    self.save_common_commands()
                    update_cmd_listbox()
                    # 更新下拉菜单
                    self.cmd_menu['values'] = list(self.common_commands.keys())

        ttk.Button(frame_buttons, text="添加", command=add_common_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_buttons, text="修改", command=edit_common_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_buttons, text="删除", command=delete_common_command).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_buttons, text="确定", command=config_window.destroy).pack(side=tk.RIGHT)

    def on_command_select(self, event):
        """处理常用命令选择事件"""
        selected_text = self.cmd_menu_var.get()
        if selected_text != "选择常用命令..." and selected_text in self.common_commands:
            command = self.common_commands[selected_text]
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, command)
            self.execute_command()

    def execute_command(self):
        """执行输入框中的命令"""
        command = self.command_input.get().strip()
        if not command:
            return

        # 恢复Python路径处理逻辑
        # 尝试从环境变量中获取Python路径
        python_path = 'python.exe'  # 默认值
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序
            python_path = sys.executable
        else:
            # 尝试使用与批处理文件相同的Python路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            python_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app', 'python-win'))
            python_exe = os.path.join(python_dir, 'python.exe')
            if os.path.exists(python_exe):
                python_path = python_exe

        # 检查是否是Python命令，如果是则使用完整路径
        if 'python' in command.lower() and not command.lower().startswith('pythonw'):
            command_parts = command.split(' ')
            if command_parts[0].lower() == 'python':
                command_parts[0] = python_path
                command = ' '.join(command_parts)

        self.status_var.set(f"正在执行命令: {command}")
        if self.output_text:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"\n===== 开始执行命令: {command} =====\n")
            self.output_text.see(tk.END)
            self.output_text.config(state=tk.DISABLED)

        try:
            # 使用subprocess.Popen实时捕获输出
            # 对于Windows命令，使用shell=True来支持命令解析
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                      text=True, bufsize=1, shell=True)
            self.current_process = process  # 保存进程引用

            # 实时更新文本框内容
            def update_output():
                if process.poll() is None:
                    line = process.stdout.readline()
                    if line:
                        if self.output_text:
                            self.output_text.config(state=tk.NORMAL)
                            self.output_text.insert(tk.END, line)
                            self.output_text.see(tk.END)
                            self.output_text.config(state=tk.DISABLED)
                    self.root.after(100, update_output)
                else:
                    # 读取剩余输出
                    remaining = process.stdout.read()
                    if remaining and self.output_text:
                        self.output_text.config(state=tk.NORMAL)
                        self.output_text.insert(tk.END, remaining)
                        self.output_text.see(tk.END)
                        self.output_text.config(state=tk.DISABLED)
                    
                    if self.output_text:
                        self.output_text.config(state=tk.NORMAL)
                        self.output_text.insert(tk.END, f"\n===== 命令执行 {'完成' if process.returncode == 0 else '失败'} =====\n")
                        self.output_text.see(tk.END)
                        self.output_text.config(state=tk.DISABLED)
                    
                    # 更新状态栏
                    if process.returncode == 0:
                        self.status_var.set(f"命令执行完成")
                    else:
                        self.status_var.set(f"命令执行失败")
                        messagebox.showerror("错误", f"命令执行失败，返回码: {process.returncode}")
                    
                    # 根据复选框状态决定是否清除输入框内容
                    if not self.keep_input_var.get():
                        self.command_input.delete(0, tk.END)

            update_output()
        except Exception as e:
            self.status_var.set(f"命令执行失败")
            messagebox.showerror("错误", f"执行命令时出错: {str(e)}")
            if self.output_text:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"\n执行命令时出错: {str(e)}\n")
                self.output_text.see(tk.END)
                self.output_text.config(state=tk.DISABLED)

    def clear_output(self):
        """清除输出窗口内容"""
        if self.output_text:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.config(state=tk.DISABLED)

    def run_command_with_output(self, command, description):
        """运行命令并在输出窗口显示结果"""
        self.status_var.set(f"{description}...")
        if self.output_text:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"===== 开始 {description} =====")
            self.output_text.see(tk.END)
            self.output_text.config(state=tk.DISABLED)

        try:
            # 使用subprocess.Popen实时捕获输出
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            self.current_process = process  # 保存进程引用

            # 调用类方法update_output
            self.update_output(process, description)
            return process
        except Exception as e:
            self.status_var.set(f"{description} 失败")
            messagebox.showerror("错误", f"{description} 时出错：{str(e)}")

    def update_output(self, process, description):
        """更新输出窗口内容"""
        if process is None:
            # 直接输出描述信息
            if self.output_text:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"===== {description} =====")
                self.output_text.see(tk.END)
                self.output_text.config(state=tk.DISABLED)
            self.status_var.set(description)
            return

        if process.poll() is None:
            line = process.stdout.readline()
            if line:
                if self.output_text:
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.insert(tk.END, line)
                    self.output_text.see(tk.END)
                    self.output_text.config(state=tk.DISABLED)
            self.root.after(100, lambda: self.update_output(process, description))
        else:
            # 读取剩余输出
            remaining = process.stdout.read()
            if remaining and self.output_text:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, remaining)
                self.output_text.see(tk.END)
                self.output_text.config(state=tk.DISABLED)
            self.current_process = None  # 进程结束，清除引用
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"===== {description} {'完成' if process.returncode == 0 else '失败'} =====")
            self.output_text.see(tk.END)
            self.output_text.config(state=tk.DISABLED)
            # 更新状态栏
            if process.returncode == 0:
                self.status_var.set(f"{description} 完成")
            else:
                self.status_var.set(f"{description} 失败")
                messagebox.showerror("错误", f"{description} 失败")

    def stop_command(self):
        """停止当前正在执行的命令"""
        if self.current_process and self.current_process.poll() is None:
            try:
                # 在Windows上终止进程
                if platform.system() == "Windows":
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(self.current_process.pid)])
                else:
                    # 在Unix/Linux/Mac上终止进程
                    self.current_process.terminate()
                    self.current_process.wait(timeout=5)
                self.update_output(None, "命令已停止")
            except Exception as e:
                self.update_output(None, f"停止命令时出错: {str(e)}")
