# Set-ExecutionPolicy RemoteSigned

# Parameter help description
param (
    $url
)

# Test if C:\Temp exists, create if no
$TLS1_PATH = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client"
$TLS2_PATH = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client"
$TLS1 = Test-Path $TLS1_PATH
$TLS2 = Test-Path $TLS2_PATH
if (!($TLS1)) {
    New-Item -Path $TLS1_PATH
    New-ItemProperty -Path $TLS1_PATH -Name "DisabledByDefault" -Value 0 -PropertyType "DWORD"
}
else {
    Write-Host "TLS1 Already exists" -ForegroundColor Green
}

if (!($TLS2)) {
    New-Item -Path $TLS2_PATH
    New-ItemProperty -Path $TLS2_PATH -Name "DisabledByDefault" -Value 0 -PropertyType "DWORD"
}
else {
    Write-Host "TLS2 Already exists" -ForegroundColor Green
}

if (Test-Path "C:\Temp") {
    Write-Host "Temp already exists" -ForegroundColor Green
}
else {
    Write-Host "Creating temp folder: C:\Temp"
    New-Item -Path "C:\" -Name "Temp" -ItemType "directory"
}
Try {
    Import-Module BitsTransfer -ErrorAction Stop
    Start-BitsTransfer -Source https://app.ninjarmm.com/agent/installer/2bba9e12-1c0c-4c1f-bb20-2d6723653d2b/daytonstudios-5.9.1158-windows-installer.msi -Destination "C:\temp\nOneInstaller.msi" -ErrorAction Stop
}
Catch {
    Write-Host "An Error Occured"
    Write-Host $_
}


Write-Host "An error occured" -ForegroundColor Red



Start-Process msiexec.exe -Wait -Verb runAs -ArgumentList '/i C:\Temp\nOneInstaller.msi /quiet'
