param (
    [Parameter()]
    [string] $prefix = $env:prefix,

    [Parameter()]
    $Reboot = $env:reboot,

    [Parameter()]
    [string] $serviceTag = $env:serviceTag
)

Try {
    if ($serviceTag -eq "") {
        $serviceTag = (Get-WmiObject -Class Win32_Bios).Serialnumber
    }
}
Catch {
    Write-Host "Service Tag Error"
}


$newComputerName = "$prefix-$serviceTag"

Try {
    Rename-Computer -NewName $newComputerName
    Write-Host "The computer has been renamed to '$newComputerName'. Please restart your computer for the changes to take effect."
    $nameSuccess = $true
}
Catch {
    Write-Host "Could not set name to '$newComputerName'"
}




if ($Reboot -eq "true" -and $nameSuccess) {
    Write-Warning -Message "Reboot specified scheduling reboot for $((Get-Date).AddMinutes(5))..."
    Start-Process "shutdown.exe" -ArgumentList "/r /t 0" -NoNewWindow -Wait
}
else {
    Write-Warning -Message "This script takes effect after a reboot. Use the reboot checkbox to have this script reboot for you."
}
