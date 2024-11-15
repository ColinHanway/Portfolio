# Set-ExecutionPolicy RemoteSigned

# Parameter help description
param (
    $url
)

# Test if C:\Temp exists, create if no
if (Test-Path "C:\Temp") {
    Write-Host "Temp already exists" -ForegroundColor Green
}
else {
    Write-Host "Creating temp folder: C:\Temp"
    New-Item -Path "C:\" -Name "Temp" -ItemType "directory"
}
try {
    Import-Module BitsTransfer -ErrorAction Stop
    Start-BitsTransfer -Source $url -Destination "C:\temp\nOneInstaller.msi" -ErrorAction Stop
}
catch [System.InvalidOperationException] {
    Write-Host "Caught exception"
}
catch {
    Write-Host "Uncaught exception"
}


Write-Host "An error occured" -ForegroundColor Red



Start-Process msiexec.exe -Wait -Verb runAs -ArgumentList '/i C:\Temp\nOneInstaller.msi /quiet'
