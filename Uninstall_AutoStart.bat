@echo off
color 0C
echo ========================================================
echo       VISIONCARE(TM) - OCULAR PROTECTION SYSTEM
echo ========================================================
echo Menghapus VisionCare dari Startup Windows...
echo.

set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OcularCareProtocol.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo [SUKSES] VisionCare berhasil dihapus dari Startup.
    echo Aplikasi tidak akan lagi otomatis menyala.
) else (
    echo [INFO] Shortcut Startup tidak ditemukan. Mungkin belum di-install.
)
echo.
pause
