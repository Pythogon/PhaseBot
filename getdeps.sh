#!/usr/bin/sh

while getopts "vh" opt
do
   case "$opt" in
      v ) verbose=1 ;;
      h ) help=1 ;;
      ? ) help=1 ;;
   esac
done

if [ $help ]; then
    echo
    echo "Usage: $0 [options]"
    echo
    echo "-v        Enable verbose output of installation"
    echo "-h        Show this menu"
    exit
fi

if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found on the PATH, please install python for your system from https://www.python.org/downloads/"
    exit
fi

if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found on the PATH, install? [y/n]"
    read installpip
    if [ $installpip = 'y' ]; then
        if [ $verbose ]; then
            echo "Installing pip3... (Verbose)"
            python3 -m ensurepip --upgrade
        else
            echo "Installing pip3..."
            python3 -m ensurepip --upgrade &> /dev/null
        fi
    else
        echo "Please install pip3 or add it to the PATH in order to use this script"
        exit
    fi
fi

if [ $verbose ]; then
    cat Depfile | while read line; do
        echo "Installing $line... (Verbose)"
        pip3 install $line 
    done
else
    cat Depfile | while read line; do
        echo "Installing $line...."
        pip3 install $line &> /dev/null
    done
fi
