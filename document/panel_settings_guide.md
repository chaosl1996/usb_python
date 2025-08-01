# U盘Python环境管理器 - 面板设置指导手册

## 一、概述
本手册详细介绍了U盘Python环境管理器的面板设置功能，包括默认按钮配置、自定义按钮管理以及面板布局调整等操作。通过本指南，您可以根据个人需求定制程序界面，提高工作效率。

## 二、面板配置文件
面板设置主要由`function/base/panel_config.json`文件控制，该文件定义了按钮的顺序、类型和功能。

### 文件位置
g:\Documents\Python\function\base\panel_config.json

### 文件结构
```json
{
    "button_order": [
        "更新库",
        "安装新库",
        "执行Python程序",
        "打开命令行",
        "刷新面板"
    ],
    "custom_buttons": [
        {
            "name": "Hello World",
            "script_path": "script\\hello_world.py",
            "description": "运行Hello World示例脚本"
        }
    ]
}
```

- `button_order`: 定义默认按钮的显示顺序
- `custom_buttons`: 存储自定义按钮的配置信息
  - `name`: 按钮显示名称
  - `script_path`: 按钮点击后执行的脚本路径
  - `description`: 按钮功能描述

## 三、面板管理器
面板设置由`function/panel_manager.py`文件中的`PanelManager`类实现，负责加载配置、管理按钮和更新界面。

### 核心功能
1. 加载配置文件
2. 生成按钮面板
3. 管理自定义按钮（添加、删除、重命名）
4. 保存配置更改

## 四、使用方法
### 4.1 基本操作
1. **启动程序**：双击`start_windows.bat`或`启动.lnk`快捷方式
2. **主界面**：程序启动后会显示默认按钮面板
3. **功能按钮**：点击相应按钮执行对应功能

### 4.2 自定义按钮管理
1. **添加自定义按钮**
   - 点击"刷新面板"按钮右侧的下拉箭头
   - 选择"添加自定义按钮"
   - 在弹出窗口中填写按钮名称、选择脚本文件并添加描述
   - 点击"确定"按钮完成添加
   - 新按钮会显示在面板末尾

2. **重命名自定义按钮**
   - 右键点击要重命名的自定义按钮
   - 选择"重命名"
   - 输入新名称并点击"确定"

3. **删除自定义按钮**
   - 右键点击要删除的自定义按钮
   - 选择"删除"
   - 在确认对话框中点击"是"

### 4.3 调整按钮顺序
1. 打开`function/base/panel_config.json`文件
2. 修改`button_order`数组中按钮的顺序
3. 保存文件并重启程序，或点击"刷新面板"按钮

## 五、高级配置
### 5.1 批量导入自定义按钮
1. 准备一个包含自定义按钮配置的JSON文件，格式如下：
   ```json
   {
       "custom_buttons": [
           {
               "name": "按钮1",
               "script_path": "script\\script1.py",
               "description": "按钮1描述"
           },
           {
               "name": "按钮2",
               "script_path": "script\\script2.py",
               "description": "按钮2描述"
           }
       ]
   }
   ```
2. 替换`function/base/panel_config.json`文件中的`custom_buttons`部分
3. 刷新面板或重启程序

### 5.2 添加新的默认功能按钮
> 注意：此操作需要修改源代码

1. 在`function`目录下创建新的功能模块（如`new_feature.py`）
2. 实现功能函数
3. 在`main.py`中导入并注册新功能
4. 在`panel_config.json`的`button_order`中添加新按钮名称
5. 重启程序

## 六、常见问题
1. **自定义按钮不显示**
   - 检查`panel_config.json`文件格式是否正确
   - 确认脚本路径是否存在且正确
   - 点击"刷新面板"按钮或重启程序

2. **按钮顺序未更新**
   - 确保`panel_config.json`文件已保存
   - 尝试重启程序

3. **无法添加自定义按钮**
   - 确保脚本目录存在且有写入权限
   - 检查脚本文件是否存在

## 七、示例配置
以下是一个完整的`panel_config.json`示例：
```json
{
    "button_order": [
        "更新库",
        "安装新库",
        "执行Python程序",
        "打开命令行",
        "刷新面板"
    ],
    "custom_buttons": [
        {
            "name": "Hello World",
            "script_path": "script\\hello_world.py",
            "description": "运行Hello World示例脚本"
        },
        {
            "name": "MD转HTML",
            "script_path": "script\\md_to_html.py",
            "description": "将Markdown文件转换为HTML"
        }
    ]
}
```

通过本指南，您可以轻松定制U盘Python环境管理器的面板设置，使其更符合个人使用习惯和工作需求。