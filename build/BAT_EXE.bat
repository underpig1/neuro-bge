@echo off
set target=%~dp1%~n1.exe
set name=%~nx1
set dir=%~dp1
set sed=%temp%\2exe.sed
(
   echo [Version]
   echo Class=IEXPRESS
   echo SEDVersion=3
   echo [Options]
   echo PackagePurpose=InstallApp
   echo ShowInstallProgramWindow=0
   echo HideExtractAnimation=1
   echo UseLongFileName=1
   echo InsideCompressed=0
   echo CAB_FixedSize=0
   echo CAB_ResvCodeSigning=0
   echo RebootMode=N
   echo InstallPrompt=%%InstallPrompt%%
   echo DisplayLicense=%%DisplayLicense%%
   echo FinishMessage=%%FinishMessage%%
   echo TargetName=%%TargetName%%
   echo FriendlyName=%%FriendlyName%%
   echo AppLaunched=%%AppLaunched%%
   echo PostInstallCmd=%%PostInstallCmd%%
   echo AdminQuietInstCmd=%%AdminQuietInstCmd%%
   echo UserQuietInstCmd=%%UserQuietInstCmd%%
   echo SourceFiles=SourceFiles
   echo [Strings]
   echo InstallPrompt=
   echo DisplayLicense=
   echo FinishMessage=
   echo FriendlyName=
   echo PostInstallCmd=^<None^>
   echo AdminQuietInstCmd=
   echo AppLaunched=cmd /c "%name%"
   echo TargetName="%target%"
   echo FILE0="%name%"
   echo FILE1="build.py"
   echo FILE2="build.blend"
   echo [SourceFiles]
   echo SourceFiles0="%dir%"
   echo [SourceFiles0]
   echo %%FILE0%%=
   echo %%FILE1%%=
   echo %%FILE2%%=
) > "%sed%"
iexpress /n /q /m %sed%
del /q /f "%sed%"
exit /b 0
