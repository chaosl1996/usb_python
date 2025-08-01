# Tkinter库配置指南

## 一、Tkinter简介
Tkinter是Python的标准GUI库，它提供了创建图形用户界面的功能。本项目的主程序`main.py`使用Tkinter构建界面，因此需要确保Tkinter正确安装和配置。

## 二、检查Tkinter是否已安装
1. **打开Python解释器**
   - 双击`start_windows.bat`启动程序
   - 或打开命令提示符，导航到`app\python-win`目录，运行`python.exe`

2. **运行以下代码**
   ```python
   import tkinter
   print(tkinter.TkVersion)