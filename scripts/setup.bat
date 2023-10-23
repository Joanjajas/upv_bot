@echo off
setlocal enabledelayedexpansion

:: Set the paths and variables
set "scripts_dir=%~dp0"
set "root_dir=%scripts_dir%.."
set "plist_file=%root_dir%\reservation_bot.plist"
set "install_dir=C:\Program Files\reservation_bot"

:: Main function
call :main
exit /b 0

:: Install the necessary python dependencies
:install_deps
echo.
echo Installing dependencies...
pip install playwright
pip install playwright-chromium
exit /b 0

:: Prompt for username and password
:get_credentials
echo Enter your intranet username and password:
set /p "username=Dni: "
set /p "password=Password: "
echo.
goto :eof

:: Check that the credentials are correct
:check_credentials
:check_credentials_loop
echo Checking if the intranet username and password are valid...
python "%scripts_dir%\check_credentials.py" "%username%" "%password%"
if %errorlevel% equ 0 (
    goto :eof
) else (
    echo The intranet username or password are not valid.
    echo.
    goto :get_credentials
)

:: Install the script in the system
:install_script
if exist "%install_dir%" (
    rmdir /s /q "%install_dir%"
)
xcopy /s /i "%root_dir%\bot" "%install_dir%"
exit /b 0

:: Replace the credentials in the script
:replace_credentials
set "script_path=%install_dir%\bot.py"
if exist "%script_path%" (
    for /f "tokens=*" %%A in ('type "%script_path%" ^| find /i "USERNAME = "') do (
        set "line=%%A"
        set "line=!line:.*=USERNAME = "!username!"!"
        echo !line!>> "%script_path%.new"
    )
    for /f "tokens=*" %%A in ('type "%script_path%.new" ^| find /i "PASSWORD = "') do (
        set "line=%%A"
        set "line=!line:.*=PASSWORD = "!password!"!"
        echo !line!>> "%script_path%.new"
    )
    move /y "%script_path%.new" "%script_path%"
)
exit /b 0

:: Create the necessary directories and files
:create_dirs
if not exist "%userprofile%\bot_reservas" (
    mkdir "%userprofile%\bot_reservas"
)
if not exist "%userprofile%\bot_reservas\reservas.toml" (
    copy "%root_dir%\reservas.toml" "%userprofile%\bot_reservas\"
)
exit /b 0

:: Create the launch agent
:create_launch_agent
if exist "%userprofile%\AppData\Local\reservation_bot\reservation_bot.xml" (
    schtasks /Delete /F /TN reservation_bot
)
schtasks /Create /TN reservation_bot /TR "%install_dir%\bot.py" /SC ONLOGON /RU %username% /RP %password%
exit /b 0

:: Main function
:main
:: Prompt for admin rights
powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList '%*'" >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run this script as an administrator.
    exit /b 1
)

:: Check for internet connection
ping -n 2 google.com >nul
if errorlevel 1 (
    echo There is no internet connection.
    echo Internet connection is needed for running this setup script.
    echo Please, connect to the internet and try again.
    exit /b 1
)

:: Call the individual functions
call :install_deps
call :get_credentials
call :check_credentials
call :install_script
call :replace_credentials
call :create_dirs
call :create_launch_agent
exit /b 0

