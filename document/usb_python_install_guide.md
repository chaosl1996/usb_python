# U盘Python环境安装配置指南

## 一、项目概述
本指南详细介绍如何在U盘中安装和配置独立的Python环境，使其可以在任何Windows电脑上使用，无需本地安装Python。

## 二、系统要求
- 操作系统：Windows 7或更高版本
- U盘空间：至少500MB可用空间
- 无需预先安装Python

## 三、下载Python嵌入式版本
1. **访问Python官方网站**
   打开浏览器，访问 https://www.python.org/downloads/windows/

2. **下载嵌入式版本**
   - 滚动到页面底部，找到"Embedded distributions"部分
   - 下载适合您系统的嵌入式版本(通常选择最新的稳定版本)
   - 确保下载的是32位或64位版本，根据您计划使用的电脑系统选择

## 四、安装Python到U盘
1. **解压下载的文件**
   - 找到下载的zip文件，右键选择"解压到当前文件夹"
   - 解压后会得到一个类似"python-3.11.4-embed-amd64"的文件夹

2. **移动到U盘**
   - 将解压后的文件夹复制到U盘的`app`目录下
   - 重命名为`python-win`，以便于使用

3. **验证安装**
   - 打开命令提示符
   - 导航到U盘的`app\python-win`目录
   - 运行`python.exe --version`，如果显示Python版本号，则安装成功

## 五、配置pip
1. **下载get-pip.py**
   - 访问 https://bootstrap.pypa.io/get-pip.py
   - 右键点击页面，选择"另存为"，保存到U盘的`app`目录

2. **安装pip**
   - 打开命令提示符
   - 导航到U盘的`app`目录
   - 运行`python-win\python.exe get-pip.py`
   - 等待安装完成

3. **验证pip**
   - 运行`python-win\Scripts\pip.exe --version`，如果显示pip版本号，则安装成功

## 六、修改启动脚本
1. **修改start_windows.bat**
   - 用文本编辑器打开U盘根目录的`start_windows.bat`
   - 确保包含以下内容：
     ```batch
     @echo off
     set PYTHON_HOME=%~dp0app\python-win
     set PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%
     cd /d %~dp0app
     python.exe main.py
     pause
     ```
   - 保存文件

## 七、安装依赖库
1. **创建requirements.txt**
   - 在U盘的`app`目录创建`requirements.txt`文件
   - 内容如下:
     ```
     pip>=23.1.2
     setuptools>=67.7.2
     wheel>=0.40.0
     ```

2. **安装依赖**
   - 打开命令提示符
   - 导航到U盘的`app`目录
   - 运行`python-win\Scripts\pip.exe install -r requirements.txt`
   - 等待安装完成

## 八、测试环境
1. **运行主程序**
   - 双击U盘根目录的`start_windows.bat`
   - 如果一切正常，会显示Python环境管理器界面

2. **测试功能**
   - 尝试使用各个功能按钮，确保它们能正常工作
   - 特别是"查看版本"功能，可以验证Python和库的版本

## 九、常见问题解决
1. **Python无法运行**
   - 检查`app\python-win`目录是否存在
   - 确保`python.exe`位于该目录下

2. **pip无法运行**
   - 检查`app\python-win\Scripts`目录是否存在`pip.exe`
   - 如果没有，重新运行`get-pip.py`安装

3. **库安装失败**
   - 检查网络连接
   - 尝试使用国内镜像源:
     ```
     python-win\Scripts\pip.exe install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
     ```

通过以上步骤，您可以在U盘的app目录下成功安装Python环境并配置所需的依赖库。