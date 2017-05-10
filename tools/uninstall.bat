ECHO shutdonw staf in case
staf local shutdown shutdown

ECHO step 1: go to staf uninstall dir
C:
cd C:\STAF\Uninstall_STAF

ECHO step 2: run the uninstall exe
Uninstall_STAF.exe

ECHO step 3: rm the STAF dir
cd C:\
rd /s/q C:\STAF
