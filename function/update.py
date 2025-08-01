# -*- coding: utf-8 -*-
"""
Python库更新脚本
此脚本用于更新已安装的库
"""
import os
import sys
import subprocess
import platform
import concurrent.futures
from tqdm import tqdm

# 设置最大并发数（根据系统内存和CPU核心数调整）
MAX_WORKERS = 4

def update_single_library(lib_name):
    """更新单个库"""
    try:
        # 使用check_output获取详细输出
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", lib_name],
            capture_output=True,
            text=True,
            timeout=300  # 设置5分钟超时
        )
        if result.returncode == 0:
            return (lib_name, True, "更新成功")
        else:
            return (lib_name, False, f"更新失败: {result.stderr[:100]}...")
    except Exception as e:
        return (lib_name, False, f"更新出错: {str(e)}")

def update_libraries():
    """更新已安装的库"""
    print("正在更新pip...")
    try:
        # 优先更新pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip更新成功！")
    except subprocess.CalledProcessError as e:
        print(f"pip更新失败: {e}")
        # 即使pip更新失败，也继续尝试更新其他库

    print("正在获取已安装的库列表...")
    try:
        # 获取已安装的库列表
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze", "--local"],
            capture_output=True,
            text=True
        )
        libraries = result.stdout.splitlines()

        # 提取库名称
        lib_names = []
        for lib in libraries:
            # 跳过编辑模式的库
            if lib.startswith("-e"):
                continue
            # 提取库名称
            lib_name = lib.split("==")[0]
            lib_names.append(lib_name)

        print(f"发现 {len(lib_names)} 个需要更新的库")

        # 使用线程池并行更新库
        print("开始并行更新库...")
        success_count = 0
        fail_count = 0

        # 使用tqdm显示进度
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # 提交所有任务
            futures = {executor.submit(update_single_library, lib_name): lib_name for lib_name in lib_names}

            # 使用tqdm迭代完成的任务
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(lib_names)):
                lib_name, success, message = future.result()
                if success:
                    success_count += 1
                    # 仅在详细模式下打印成功信息
                    # print(f"{lib_name} 更新成功！")
                else:
                    fail_count += 1
                    print(f"{lib_name} {message}")

        print(f"库更新完成！成功: {success_count}, 失败: {fail_count}")

    except Exception as e:
        print(f"更新库时出错: {e}")

if __name__ == "__main__":
    print("===== 库更新工具 ======")
    update_libraries()