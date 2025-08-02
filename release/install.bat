@echo off
echo 🔍 ExcelSearchPro Installation
echo ==============================
echo.

echo 📁 Creating installation directory...
set "INSTALL_DIR=%USERPROFILE%\ExcelSearchPro"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 📦 Copying files...
copy "ExcelSearchPro.exe" "%INSTALL_DIR%\" >nul
copy "ExcelSearchPro-GUI.exe" "%INSTALL_DIR%\" >nul  
copy "ExcelSearchPro-CLI.exe" "%INSTALL_DIR%\" >nul
if exist "README.md" copy "README.md" "%INSTALL_DIR%\" >nul

echo 🔗 Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\ExcelSearchPro.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\ExcelSearchPro.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "ExcelSearchPro - Fast Excel Database Search" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul 2>&1
del CreateShortcut.vbs >nul 2>&1

echo.
echo ✅ Installation complete!
echo 📍 Installed to: %INSTALL_DIR%
echo 🖥️  Desktop shortcut created
echo 🚀 Double-click desktop shortcut to run
echo.
echo 💡 You can also run directly:
echo    • ExcelSearchPro.exe - Main launcher with menu
echo    • ExcelSearchPro-GUI.exe - Direct GUI launch
echo    • ExcelSearchPro-CLI.exe - Command-line version
echo.
pause
