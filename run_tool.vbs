Set fso = CreateObject("Scripting.FileSystemObject")
Set ws = CreateObject("WScript.Shell")

dir = fso.GetParentFolderName(WScript.ScriptFullName)
ws.CurrentDirectory = dir

pyExe = "D:\NetworkCoordinator\.venv\Scripts\pythonw.exe"
If Not fso.FileExists(pyExe) Then
    pyExe = ws.ExpandEnvironmentStrings("%USERPROFILE%") & "\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\pythonw.exe"
End If
If Not fso.FileExists(pyExe) Then
    pyExe = "pythonw.exe"
End If

ws.Run """" & pyExe & """ """ & dir & "\exam_harvester_tool.py""", 0, False
