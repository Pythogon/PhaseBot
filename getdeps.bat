@echo off
setlocal

set verbose=0

:loop
    if x%1 equ x goto done
    set param=%1
    if %param:~0,1% equ - goto checkopt

:invalid_param
    echo "Invalid option: %1" 
:help
    echo "Usage: %0 [options]"
    echo "-v        Enable verbose output of installation"
    echo "-h        Show this menu"
    exit

:next
    shift /1
    goto loop

:checkopt
    if "%1" equ "-v" goto setverbose
    if "%1" equ "-h" goto help
    goto invalid_param

:setverbose
    shift /1
    set verbose=1

:done

where python >nul 2>&1 && (
    goto pip
) || (
    echo "python could not be found on the PATH, please install python for your system from https://www.python.org/downloads/"
    exit
)

:pip
where pip >nul 2>&1 && (
    goto dependencies
) || (
    set /p installpip="pip could not be found on the PATH, install? [y/n]"
    if "%installpip%" == "y" (
        if %verbose% == 1 (
            echo "Installing pip3... (Verbose)"
            python -m ensurepip --upgrade
        ) else (
            echo "Installing pip3..."
            python -m ensurepip --upgrade >nul
        )
    ) else (
        echo "Please install pip3 or add it to the PATH in order to use this script"
        exit
    )
    exit
)

:dependencies
if %verbose% == 1 (
    for /F "tokens=*" %%line in (Depfile) do (
        echo "Installing "%%line"... (Verbose)"
        pip install %%line 
    )
) else (
    for /F "tokens=*" %%line in (Depfile) do (
        echo "Installing "%%line"..."
        pip install %%line >nul
    )
)
