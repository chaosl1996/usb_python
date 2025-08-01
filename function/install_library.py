#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
库安装脚本
此脚本用于安装新的Python库
"""
import os
import sys
import subprocess

def install_library(lib_name):
    """安装指定的库"""
    if not lib_name:
        print("错误: 请提供库名称")
        return False

    print(f"正在安装库: {lib_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib_name])
        print(f"库 {lib_name} 安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装库 {lib_name} 失败: {e}")
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        return False

if __name__ == "__main__":
    print("===== Python库安装工具 ======")
    if len(sys.argv) > 1:
        lib_name = sys.argv[1]
        install_library(lib_name)
    else:
        lib_name = input("请输入要安装的库名称: ").strip()
        install_library(lib_name)