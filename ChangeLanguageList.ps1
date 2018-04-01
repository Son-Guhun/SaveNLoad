ipmo international
$oldLangList = Get-WinUserLanguageList
Set-WinUserLanguageList -Force 'en-US'
echo 'Done!'
$PIPE = Read-Host -Prompt 'Enter input to restore langugage'
Set-WinUserLanguageList -Force $oldLangList