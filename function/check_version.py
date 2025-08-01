#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
版本信息查看脚本
此脚本用于查看Python及已安装库的版本信息
"""
import os
import sys
import subprocess

def check_python_version():
    """查看Python版本"""
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"Python路径: {sys.executable}")


def check_libraries_version():
    """查看已安装库的版本"""
    print("\n已安装库列表:")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"获取库列表失败: {e}")

if __name__ == "__main__":
    print("===== Python版本信息 ======")
    check_python_version()
    print("\n===== 已安装库版本信息 ======")
    check_libraries_version()