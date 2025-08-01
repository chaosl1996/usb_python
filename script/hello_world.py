#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例程序:  Hello World
这是一个简单的Python示例程序
"""

def say_hello(name):
    """向指定的人问好"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print("===== 示例程序: Hello World ======")
    name = input("请输入您的名字: ").strip()
    if not name:
        name = "World"
    message = say_hello(name)
    print(message)
    print("\n这是一个简单的Python示例程序。")
    print("您可以在script文件夹中创建更多的Python程序。")
    input("按Enter键退出...")