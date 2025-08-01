Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "g:\Documents\Python\app\start_windows.bat" & chr(34), 0
Set WshShell = Nothing