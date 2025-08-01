# -*- coding: utf-8 -*-
"""
Markdown转HTML工具
此脚本用于将Markdown文档转换为HTML格式
"""
import os
import sys
import argparse
from datetime import datetime

# 检查是否安装了markdown库
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

def convert_md_to_html(input_dir, output_dir):
    """
    将指定目录下的所有Markdown文件转换为HTML
    
    参数:
    input_dir -- 包含Markdown文件的目录
    output_dir -- 输出HTML文件的目录
    """
    print("===== Markdown转HTML工具 =====")
    
    # 检查markdown库是否可用
    if not MARKDOWN_AVAILABLE:
        print("错误: 未找到markdown库。请先使用'pip install markdown'安装。")
        return False
    
    # 确保输入目录存在
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 '{input_dir}' 不存在。")
        return False
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    # 获取所有Markdown文件
    md_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.md')]
    
    if not md_files:
        print(f"警告: 在目录 '{input_dir}' 中未找到Markdown文件。")
        return True
    
    # 转换每个Markdown文件
    for md_file in md_files:
        md_path = os.path.join(input_dir, md_file)
        html_file = os.path.splitext(md_file)[0] + '.html'
        html_path = os.path.join(output_dir, html_file)
        
        try:
            print(f"正在转换: {md_file} -> {html_file}")
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 转换Markdown为HTML
            html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
            
            # 添加基本的HTML结构
            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.splitext(md_file)[0]}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        h1, h2, h3, h4 {{
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 15px;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{os.path.splitext(md_file)[0]}</h1>
            <p>转换时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        <main>
            {html_content}
        </main>
        <footer>
            <p>由Markdown转HTML工具生成</p>
        </footer>
    </div>
</body>
</html>"""
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            print(f"转换成功: {html_file}")
        except Exception as e:
            print(f"转换 '{md_file}' 时出错: {e}")
    
    print("===== 转换完成 =====")
    return True

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Markdown转HTML工具')
    parser.add_argument('--input', '-i', default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'document'),
                        help='输入Markdown文件目录 (默认: 项目document目录)')
    parser.add_argument('--output', '-o', default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'html_docs'),
                        help='输出HTML文件目录 (默认: app/html_docs目录)')
    
    args = parser.parse_args()
    
    # 执行转换
    convert_md_to_html(args.input, args.output)

if __name__ == "__main__":
    main()
    input("按Enter键退出...")