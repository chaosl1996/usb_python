import os
import json  # 添加这行导入
import importlib.util
import os  # 添加os模块导入
import sys  # 添加sys模块导入
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class PanelManager:
    def __init__(self, root, env_manager):
        self.root = root
        self.env_manager = env_manager
        self.panel_config_file = os.path.join(os.path.dirname(__file__), 'base', 'panel_config.json')
        self.functions_dir = os.path.dirname(__file__)
        self.script_dir = os.path.join(os.path.dirname(self.functions_dir), 'script')
        
        # 加载面板配置
        self.load_panel_config()
        
        # 定义不可删除的默认功能
        self.default_functions = ["更新库", "安装新库", "打开命令窗口", "执行Python程序", "查看版本", "面板设置"]
        
    def load_panel_config(self):
        """加载面板配置"""
        if os.path.exists(self.panel_config_file):
            try:
                with open(self.panel_config_file, 'r', encoding='utf-8') as f:
                    self.panel_config = json.load(f)
                # 应用保存的按钮顺序
                if 'button_order' in self.panel_config and self.panel_config['button_order']:
                    ordered_buttons = []
                    # 先添加配置中的按钮
                    for btn_text in self.panel_config['button_order']:
                        found = False
                        for btn in self.env_manager.buttons:
                            if btn[0] == btn_text:
                                ordered_buttons.append(btn)
                                found = True
                                break
                        # 如果没找到，可能是自定义按钮，尝试重建
                        if not found and 'custom_buttons' in self.panel_config:
                            for custom_btn in self.panel_config['custom_buttons']:
                                if custom_btn['name'] == btn_text:
                                    # 重建自定义按钮
                                    file_path = custom_btn['file_path']
                                    
                                    def create_wrapper(file_path, display_name):
                                        def wrapper():
                                            self.env_manager.update_status(f"正在执行{display_name}...")
                                            try:
                                                # 自动显示输出窗口
                                                self.env_manager.output_manager.show_output_window()
                                                # 运行命令并显示输出
                                                self.env_manager.output_manager.run_command_with_output([sys.executable, file_path], display_name)
                                            except Exception as e:
                                                self.env_manager.update_status(f"{display_name}执行失败")
                                                messagebox.showerror("错误", f"执行{display_name}时出错：{str(e)}")
                                        return wrapper

                                    wrapper = create_wrapper(file_path, btn_text)
                                    ordered_buttons.append((btn_text, wrapper))
                                    # 添加到按钮列表
                                    self.env_manager.buttons.append((btn_text, wrapper))
                                    found = True
                                    break
                        if not found:
                            print(f"警告：未找到按钮 '{btn_text}' 的实现")
                    # 再添加未在配置中的按钮
                    for btn in self.env_manager.buttons:
                        btn_text = btn[0]
                        if btn_text not in self.panel_config['button_order']:
                            ordered_buttons.append(btn)
                    # 更新按钮列表
                    self.env_manager.buttons = ordered_buttons
                    print(f"成功加载配置: {self.panel_config}")
            except Exception as e:
                print(f"加载面板配置失败: {e}")
                self.panel_config = {'button_order': [], 'custom_buttons': []}
        else:
            self.panel_config = {'button_order': [], 'custom_buttons': []}
            # 保存默认配置
            self.save_panel_config()
            print("创建默认配置")

    def save_panel_config(self):
        """保存面板配置"""
        try:
            # 确保目录存在
            config_dir = os.path.dirname(self.panel_config_file)
            os.makedirs(config_dir, exist_ok=True)
            
            # 确保custom_buttons字段存在
            if 'custom_buttons' not in self.panel_config:
                self.panel_config['custom_buttons'] = []
            
            # 调试信息
            print(f"保存配置到: {self.panel_config_file}")
            print(f"配置内容: {self.panel_config}")
            
            with open(self.panel_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.panel_config, f, ensure_ascii=False, indent=2)
            
            print("配置保存成功")
        except PermissionError:
            error_msg = f"权限不足，无法写入配置文件: {self.panel_config_file}"
            print(error_msg)
            messagebox.showerror("错误", error_msg)
        except Exception as e:
            error_msg = f"保存面板配置失败: {str(e)}"
            print(error_msg)
            messagebox.showerror("错误", error_msg)

    def move_up(self, listbox):
        """将选中项上移"""
        selected = listbox.curselection()
        if not selected: return
        i = selected[0]
        if i > 0:
            text = listbox.get(i)
            listbox.delete(i)
            listbox.insert(i-1, text)
            listbox.selection_set(i-1)
            
    def move_down(self, listbox):
        """将选中项下移"""
        selected = listbox.curselection()
        if not selected: return
        i = selected[0]
        if i < listbox.size() - 1:
            text = listbox.get(i)
            listbox.delete(i)
            listbox.insert(i+1, text)
            listbox.selection_set(i+1)
            
    def rename_function(self, listbox):
        """重命名选中的功能"""
        selected = listbox.curselection()
        if not selected: return
        i = selected[0]
        old_name = listbox.get(i)
        
        # 检查是否为默认功能
        if old_name in self.default_functions:
            messagebox.showwarning("警告", "默认功能不支持重命名")
            return
        
        # 创建重命名对话框
        rename_window = tk.Toplevel(self.root)
        rename_window.title("重命名功能")
        rename_window.geometry("300x150")
        rename_window.resizable(False, False)
        rename_window.configure(bg="#f0f0f0")
        rename_window.transient(self.root)
        rename_window.grab_set()
        
        # 添加标签和输入框
        ttk.Label(rename_window, text="请输入新名称：", background="#f0f0f0").pack(pady=10)
        name_entry = ttk.Entry(rename_window, width=20, font=("Microsoft YaHei", 12))
        name_entry.pack(pady=10)
        name_entry.insert(0, old_name)
        name_entry.focus_set()
        
        def do_rename():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showwarning("警告", "名称不能为空！")
                return
            
            # 更新列表
            listbox.delete(i)
            listbox.insert(i, new_name)
            listbox.selection_set(i)
            
            # 更新按钮列表
            for j, (text, command) in enumerate(self.env_manager.buttons):
                if text == old_name:
                    self.env_manager.buttons[j] = (new_name, command)
                    break
            
            # 重建按钮面板
            self.env_manager.rebuild_button_panel()
            rename_window.destroy()
        
        # 添加按钮
        button_frame = ttk.Frame(rename_window)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="确认", command=do_rename).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=rename_window.destroy).pack(side=tk.LEFT, padx=10)
        
    def delete_function(self, listbox):
        """删除选中的功能"""
        selected = listbox.curselection()
        if not selected: return
        i = selected[0]
        function_name = listbox.get(i)
        
        # 检查是否为默认功能
        if function_name in self.default_functions:
            messagebox.showwarning("警告", "默认功能不支持删除")
            return
        
        if messagebox.askyesno("确认", f"确定要删除{function_name}功能吗？"):
            # 从按钮列表中删除
            for j, (text, command) in enumerate(self.env_manager.buttons):
                if text == function_name:
                    del self.env_manager.buttons[j]
                    break
            
            # 更新列表
            listbox.delete(i)
            
            # 重建按钮面板
            self.env_manager.rebuild_button_panel()
        
    def add_function_from_script(self, listbox):
        """从script文件夹添加功能"""
        # 确保script目录存在
        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)
            messagebox.showinfo("提示", "script文件夹已创建，请将Python程序放入该文件夹后重试。")
            return
        
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择Python程序",
            initialdir=self.script_dir,
            filetypes=[("Python Files", "*.py")]
        )
        
        if not file_path:
            return
        
        # 获取文件名
        file_name = os.path.basename(file_path)
        function_name = os.path.splitext(file_name)[0]
        
        # 创建功能名称对话框
        name_window = tk.Toplevel(self.root)
        name_window.title("设置按钮名称")
        name_window.geometry("300x150")
        name_window.resizable(False, False)
        name_window.configure(bg="#f0f0f0")
        name_window.transient(self.root)
        name_window.grab_set()
        
        # 添加标签和输入框
        ttk.Label(name_window, text="请输入按钮名称：", background="#f0f0f0").pack(pady=10)
        name_entry = ttk.Entry(name_window, width=20, font=("Microsoft YaHei", 12))
        name_entry.pack(pady=10)
        name_entry.insert(0, function_name.replace('_', ' ').title())
        name_entry.focus_set()
        
        def do_add():
            display_name = name_entry.get().strip()
            if not display_name:
                messagebox.showwarning("警告", "名称不能为空！")
                return
            
            # 检查名称是否已存在
            for text, _ in self.env_manager.buttons:
                if text == display_name:
                    messagebox.showwarning("警告", f"名称'{display_name}'已存在！")
                    return
            
            # 创建包装函数
            def wrapper():
                self.env_manager.update_status(f"正在执行{display_name}...")
                try:
                    # 自动显示输出窗口
                    self.env_manager.output_manager.show_output_window()
                    # 运行命令并显示输出
                    self.env_manager.output_manager.run_command_with_output([sys.executable, file_path], display_name)
                except Exception as e:
                    self.env_manager.update_status(f"{display_name}执行失败")
                    messagebox.showerror("错误", f"执行{display_name}时出错：{str(e)}")
            
            # 添加到按钮列表
            self.env_manager.buttons.append((display_name, wrapper))
            
            # 更新列表
            listbox.insert(tk.END, display_name)
            
            # 保存自定义按钮信息
            if 'custom_buttons' not in self.panel_config:
                self.panel_config['custom_buttons'] = []
            
            # 检查是否已存在相同名称的自定义按钮
            for i, btn in enumerate(self.panel_config['custom_buttons']):
                if btn['name'] == display_name:
                    # 更新已有按钮
                    self.panel_config['custom_buttons'][i] = {'name': display_name, 'file_path': file_path}
                    break
            else:
                # 添加新按钮
                self.panel_config['custom_buttons'].append({'name': display_name, 'file_path': file_path})
            
            # 重建按钮面板
            self.env_manager.rebuild_button_panel()
            # 保存新的按钮顺序
            self.save_order(listbox)
            name_window.destroy()
        
        # 添加按钮
        button_frame = ttk.Frame(name_window)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="确认", command=do_add).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=name_window.destroy).pack(side=tk.LEFT, padx=10)
        
    def save_order(self, listbox):
        """保存排序后的顺序"""
        # 获取排序后的按钮文本
        sorted_texts = list(listbox.get(0, tk.END))
        
        # 重新排序按钮
        new_buttons = []
        for text in sorted_texts:
            for btn_text, command in self.env_manager.buttons:
                if btn_text == text:
                    new_buttons.append((btn_text, command))
                    break
        
        # 更新按钮顺序
        self.env_manager.buttons = new_buttons
        
        # 更新配置
        self.panel_config['button_order'] = sorted_texts
        self.save_panel_config()
        
        # 重建按钮面板
        self.env_manager.rebuild_button_panel()
        
    def panel_settings(self):
        """面板设置主函数"""
        # 创建设置对话框
        settings_window = tk.Toplevel(self.root)
        settings_window.title("功能面板设置")
        settings_window.geometry("600x400")
        settings_window.resizable(True, True)
        settings_window.configure(bg="#f0f0f0")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 添加窗口关闭时的回调函数
        def on_closing():
            # 直接保存更改，不询问
            self.save_order(listbox)
            settings_window.destroy()
        
        settings_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 居中显示
        settings_window.update_idletasks()
        width = settings_window.winfo_width()
        height = settings_window.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
        y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
        settings_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # 创建标题
        title_label = ttk.Label(settings_window, text="功能面板设置", font=("Microsoft YaHei", 14, "bold"))
        title_label.pack(pady=10)
        
        # 创建主框架
        main_frame = ttk.Frame(settings_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建列表框框架
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建列表框
        listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, font=("Microsoft YaHei", 12), bg="white", height=10)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        # 填充列表框
        current_buttons = self.env_manager.buttons
        for text, _ in current_buttons:
            listbox.insert(tk.END, text)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        
        # 创建按钮框架
        button_frame = ttk.Frame(main_frame, width=100)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        button_frame.pack_propagate(False)
        
        # 添加排序按钮
        ttk.Button(button_frame, text="上移", command=lambda: self.move_up(listbox), width=10).pack(pady=5)
        ttk.Button(button_frame, text="下移", command=lambda: self.move_down(listbox), width=10).pack(pady=5)
        ttk.Separator(button_frame).pack(fill=tk.X, pady=10)
        
        # 添加功能按钮
        ttk.Button(button_frame, text="重命名", command=lambda: self.rename_function(listbox), width=10).pack(pady=5)
        ttk.Button(button_frame, text="删除", command=lambda: self.delete_function(listbox), width=10).pack(pady=5)
        
        # 创建底部按钮框架
        bottom_frame = ttk.Frame(settings_window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        
        # 添加从script添加功能按钮
        ttk.Button(bottom_frame, text="从script添加功能", command=lambda: self.add_function_from_script(listbox)).pack(side=tk.LEFT, padx=10)
        
        # 添加保存和关闭按钮
        ttk.Button(bottom_frame, text="保存设置", command=lambda: self.save_order(listbox)).pack(side=tk.RIGHT, padx=10)

# 示例使用
if __name__ == "__main__":
    print("This module should be imported and used by main.py")