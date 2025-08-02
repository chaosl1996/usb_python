' 获取当前脚本所在的盘符
Set WshShell = CreateObject("WScript.Shell")
strScriptPath = WScript.ScriptFullName
strDrive = Left(strScriptPath, 1) ' 提取盘符（如 "h"）

' 使用动态盘符构建批处理文件路径
strBatPath = strDrive & ":\Documents\Python\app\start_windows.bat"

' 运行批处理文件
WshShell.Run chr(34) & strBatPath & chr(34), 0
Set WshShell = Nothing
