



pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
wheel --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
wheel version
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
