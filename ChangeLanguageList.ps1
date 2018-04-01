ipmo international
$oldLangList = Get-WinUserLanguageList
Set-WinUserLanguageList -Force 'en-US'
echo 'User languague sucessfully changed to en-US'
$PIPE = Read-Host
Set-WinUserLanguageList -Force $oldLangList