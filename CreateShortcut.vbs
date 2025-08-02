Set oWS = WScript.CreateObject("WScript.Shell") 
sLinkFile = "C:\Users\ZoZ\Desktop\ExcelSearchPro.lnk" 
Set oLink = oWS.CreateShortcut(sLinkFile) 
oLink.TargetPath = "C:\Users\ZoZ\ExcelSearchPro\ExcelSearchPro.exe" 
oLink.WorkingDirectory = "C:\Users\ZoZ\ExcelSearchPro" 
oLink.Description = "ExcelSearchPro - Fast Excel Database Search" 
oLink.Save 
