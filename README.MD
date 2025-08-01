# U盘Python环境管理器使用手册

## 项目概述
本项目是一个便携式U盘Python环境管理器，提供了一个独立的Python环境，无需在本地安装即可在不同的Windows电脑上使用。项目包含图形界面和多种实用功能，方便用户管理Python环境、安装库和执行Python程序。

## 系统要求
- 操作系统：Windows 7或更高版本
- U盘空间：至少500MB可用空间
- 无需安装Python，项目自带独立Python环境

## 目录结构
├── app/
│   ├── python-win/         # Python 3.13.5 嵌入式版本
│   ├── main.py             # 主程序入口
│   ├── start.vbs           # Windows启动脚本
│   ├── start_windows.bat   # Windows批处理启动文件
│   └── README.md           # app目录说明
├── function/
│   ├── base/               # 基础功能模块
│   │   ├── output_manager.py  # 输出管理器
│   │   ├── panel_config.json  # 面板配置文件
│   │   └── common_commands.json  # 常用命令配置
│   ├── panel_manager.py    # 面板管理器
│   ├── update.py           # 库更新脚本
│   ├── install_library.py  # 库安装脚本
│   └── check_version.py    # 版本检查脚本
├── script/
│   └── hello_world.py      # 示例脚本
├── document/
│   └── usb_python_install_guide.md  # U盘Python安装指南
│   └── common_commands_guide.md  # 常用命令列表配置指导
│   └── panel_settings_guide.md  # 面板设置指导手册
│   └── tkinter_config_guide.md  # Tkinter配置指导手册
├── readme.txt              # 文本格式说明
└── 启动.lnk                # Windows快捷方式

## 启动方法
### 方法1：使用快捷方式
- 双击U盘中的`启动.lnk`快捷方式

### 方法2：使用批处理文件
- 双击`app/start_windows.bat`批处理文件

### 方法3：使用VBS脚本
- 双击`app/start.vbs`脚本文件

## 主界面功能
启动后将显示图形界面，包含以下功能按钮：
- **更新库**：更新已安装的Python库
- **安装新库**：输入库名称安装新的Python库
- **执行Python程序**：选择并运行script文件夹中的Python脚本
- **查看版本**：查看当前Python版本和已安装库的版本
- **面板设置**：自定义功能按钮的顺序、添加或删除功能

## 详细功能说明
### 1. 更新库
点击"更新库"按钮，程序将自动更新所有已安装的Python库到最新版本。更新过程中会显示详细输出。

### 2. 安装新库
点击"安装新库"按钮，会弹出输入框，输入要安装的库名称，程序将自动下载并安装。支持使用国内镜像源加速安装。

### 3. 执行Python程序
点击"执行Python程序"按钮，会打开文件选择对话框，选择script文件夹中的Python脚本执行。如果script文件夹不存在，程序会自动创建。

### 4. 查看版本
点击"查看版本"按钮，程序将显示当前Python版本和已安装库的版本信息。

### 5. 面板设置
点击"面板设置"按钮，可以：
- 调整功能按钮的顺序
- 添加自定义功能（从script文件夹中选择Python脚本）
- 删除自定义功能
- 重命名自定义功能

## 常用命令
项目中预设了以下常用命令（可在命令输出窗口的下拉菜单中选择）：
1. **列出当前目录**：执行`dir`命令，显示当前目录内容
2. **查看Python版本**：执行`python --version`命令，显示Python版本信息

## 常见问题解决
### 1. Python无法运行
- 检查`app/python-win`目录是否存在
- 确保`python.exe`位于该目录下

### 2. pip无法运行
- 检查`app/python-win/Scripts`目录是否存在`pip.exe`
- 如果没有，重新运行`get-pip.py`安装

### 3. 库安装失败
- 检查网络连接
- 尝试使用国内镜像源：在安装命令后添加`-i https://pypi.tuna.tsinghua.edu.cn/simple`

### 4. 界面显示异常
- 确保系统已安装必要的字体
- 尝试调整窗口大小

## 注意事项
1. 本环境为便携式，无需安装，可在任何Windows电脑上使用
2. 首次使用前建议运行"查看版本"功能验证环境
3. 请不要随意删除或修改文件夹结构
4. U盘盘符变化不影响使用
5. 若遇到问题，可以查看document文件夹中的帮助文档
6. 程序退出时会自动保存面板配置

## 扩展功能
您可以通过添加自定义Python脚本来扩展程序功能：
1. 将您的Python脚本保存到script文件夹
2. 点击"面板设置"按钮
3. 点击"从script文件夹添加功能"按钮
4. 选择您的脚本并设置按钮名称
5. 新功能按钮将出现在主界面上

希望本使用手册能帮助您更好地使用U盘Python环境管理器！如有任何问题或建议，请随时联系我们。