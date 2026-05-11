@echo off
color 0B
echo ========================================================
echo       OCULUSCARE(TM) - OCULAR PROTECTION SYSTEM
echo ========================================================
echo.

echo [1/2] Memeriksa persyaratan sistem (Python)...

:: Cek via command 'python'
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Python terdeteksi di sistem via command python.
    goto :register_startup
)

:: Cek via command 'py' (Python Launcher Windows)
py --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Python terdeteksi di sistem via command py.
    goto :register_startup
)

:: Cek via command 'python3'
python3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Python terdeteksi di sistem via command python3.
    goto :register_startup
)

:: Cek manual di folder instalasi default (kalau-kalau tidak masuk PATH)
if exist "%LOCALAPPDATA%\Programs\Python" (
    echo [OK] Folder instalasi Python terdeteksi.
    goto :register_startup
)
if exist "C:\Program Files\Python*" (
    echo [OK] Folder instalasi Python terdeteksi di Program Files.
    goto :register_startup
)

:: Jika semuanya gagal, baru kita pastikan memang belum ada dan otomatis install
echo [!] Sistem mendeteksi Python benar-benar belum terinstall.
echo Mengunduh Python Installer... (Pastikan PC terhubung ke internet)
curl -# -o "%TEMP%\python_installer.exe" "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"

echo.
echo Menginstall Python secara otomatis (Background Install)...
echo Mohon tunggu beberapa menit. Mungkin akan muncul pop-up Windows User Account Control (UAC), silakan klik "Yes".
start /wait "" "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo.
echo Membersihkan file installer sementara...
del "%TEMP%\python_installer.exe"
echo [SUKSES] Python berhasil diinstall!

:install_deps
echo.
echo Menginstall pustaka yang dibutuhkan (Pystray, Pillow)...
python -m pip install pystray pillow >nul 2>&1
py -m pip install pystray pillow >nul 2>&1

:register_startup
echo.
echo [2/2] Mendaftarkan OculusCare ke Startup Windows...

set "TARGET_PATH=%~dp0OcularCareLauncher.bat"
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OcularCareProtocol.lnk"
set "WORKING_DIR=%~dp0"

powershell -Command "$wshell = New-Object -ComObject WScript.Shell; $s = $wshell.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_PATH%'; $s.WorkingDirectory = '%WORKING_DIR%'; $s.WindowStyle = 7; $s.Save()"

echo.
echo [SUKSES] OculusCare berhasil didaftarkan! 
echo Memulai aplikasi untuk pertama kali...
start "" "%TARGET_PATH%"
echo Aplikasi sudah berjalan di latar belakang.
echo.
pause
