ECHO shutdonw staf in case
staf local shutdown shutdown

ECHO step 1: install staf
STAF3426-setup-winamd64-NoJVM.exe -i silent -DACCEPT_LICENSE=1

ECHO step 2: needs copy the STAF.cfg to C:\STAF\bin dir
xcopy STAF-cli.cfg C:\STAF\bin\STAF.cfg /Y

ECHO step 3: go to staf dir
cd C:\STAF\bin

ECHO step 4: lanuch staf 
STAFProc.exe