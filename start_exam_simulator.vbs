Set ws = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

dir = fso.GetParentFolderName(WScript.ScriptFullName)
htmlFile = dir & "\sas_exam_simulator.html"

ws.Run """" & htmlFile & """", 1, False
