:: 启动Python环境
setlocal
set PYTHON_HOME=%~dp0python-win
set PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%

:: 检查Python是否可运行
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 无法找到Python环境，请确保python-win目录下有正确的Python安装。
    pause
    exit /b 1
)

:: 使用pythonw.exe启动主程序（无窗口模式）
start "" pythonw %~dp0main.py

:: 立即关闭命令窗口
exit
endlocal
