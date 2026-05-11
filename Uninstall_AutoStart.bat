@echo off
color 0C
echo ========================================================
echo       OCULUSCARE(TM) - OCULAR PROTECTION SYSTEM
echo ========================================================
echo Menghapus OculusCare dari Startup Windows...
echo.

set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OcularCareProtocol.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo [SUKSES] OculusCare berhasil dihapus dari Startup.
    echo Aplikasi tidak akan lagi otomatis menyala.
) else (
    echo [INFO] Shortcut Startup tidak ditemukan. Mungkin belum di-install.
)
echo.
pause
