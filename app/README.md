# U盘Python环境使用指南

## 环境概述
本U盘包含一个独立的Python 3.13.5环境，无需安装即可使用。该环境已配置好pip，可以安装和使用第三方包。

## 目录结构
```
app/
├── python-win/         # Python 3.13.5 嵌入式版本
├── test_installation.py  # 环境测试脚本
├── fix_package_install.py # 包安装修复脚本
├── diagnose_import.py   # 导入问题诊断脚本
└── README.md           # 使用指南
```

## 如何使用

### 1. 运行Python
直接执行以下命令：
```
app\python-win\python.exe
```

### 2. 运行Python脚本
```
app\python-win\python.exe 脚本路径
```

### 3. 使用pip安装包
```
app\python-win\python.exe -m pip install 包名
```
例如，安装requests包：
```
app\python-win\python.exe -m pip install requests
```

### 4. 使用镜像源加速安装
如果网络较慢，可以使用国内镜像源：
```
app\python-win\python.exe -m pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 测试环境
可以运行测试脚本来验证环境是否正常工作：
```
app\python-win\python.exe app\test_installation.py
```

## 注意事项
1. 本环境为便携式，无需安装，可在任何Windows电脑上使用
2. 首次使用前建议运行测试脚本来验证环境
3. 如果遇到包安装或导入问题，可以运行修复脚本：
```
app\python-win\python.exe app\fix_package_install.py
```
4. 如有其他问题，可以运行诊断脚本：
```
app\python-win\python.exe app\diagnose_import.py
```