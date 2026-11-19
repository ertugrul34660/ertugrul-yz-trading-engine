$wscript = New-Object -ComObject Wscript.Shell
$act = $wscript.AppActivate("Midas Atlas")
Write-Host "Midas Atlas Aktif mi:" $act
if (-not $act) {
    $act = $wscript.AppActivate("Google Chrome")
    Write-Host "Chrome Aktif mi:" $act
}
if ($act) {
    Start-Sleep -Milliseconds 300
    $wscript.SendKeys("{ENTER}")
    Write-Host "ENTER gonderildi!"
}
