ipmo international
Set-Variable -Name 'desc' -Value (Get-WinUserLanguageList)
Set-WinUserLanguageList -Force 'en-US'
#Remove-Item -path './me.txt'
while(( Test-Path './me.txt' -PathType Leaf) -ne $True)
     {
	Start-Sleep -s 1 
     }
Set-WinUserLanguageList -Force (Get-Variable -Name 'desc' -Value)
Remove-Item -path './me.txt'
