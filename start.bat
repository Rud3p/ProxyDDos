@echo off
title ProxyDDoS Setup
color a

echo Installing dependencies...
pip install pystyle
pip install requests
pip install os-sys
pip install sockets
pip install colorama

echo Dependencies installed!

echo ProxyDDoS Setup Complete!
echo Starting ProxyDDoS...

timeout /t 1 >nul

python ProxyDDoS.py

echo Exiting...
timeout /t 2 >nul
exit
