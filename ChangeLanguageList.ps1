ipmo international
$oldLangList = Get-WinUserLanguageList
Set-WinUserLanguageList -Force 'en-US'
Try
{
    echo 'User languague sucessfully changed to en-US'
    $PIPE = Read-Host
}
Finally
{
    Set-WinUserLanguageList -Force $oldLangList
}
