#Requires -Version 5.1

<#
.SYNOPSIS
    Removes N-Able Agent from the system.
.DESCRIPTION
    Removes N-Able Agent from the system.

    Note: Other N-Able Agent related applications will not be removed. This script can be modified to account for them if needed.
      See line 43 for more details
.EXAMPLE
    (No Parameters)

    [Info] N-Able Agent found
    [Info] Removing N-Able Agent using msiexec
    [Info] N-Able Agent successfully removed
.OUTPUTS
    None
.NOTES
    Minimum OS Architecture Supported: Windows 10, Windows Server 2016
    Release Notes: Initial Release
#>

[CmdletBinding()]
param ()

begin {
    function Test-IsElevated {
        $id = [System.Security.Principal.WindowsIdentity]::GetCurrent()
        $p = New-Object System.Security.Principal.WindowsPrincipal($id)
        $p.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
    }
}
process {
    if (-not (Test-IsElevated)) {
        Write-Error -Message "[Error] Access Denied. Please run with Administrator privileges."
        exit 1
    }

    # Get UninstallString for N-Able Agent from the registry
    $nable = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' |
    Where-Object { $_.Publisher -eq 'N-able' } |
    # Replace the line above with additions like below
    # Where-Object { $_.DisplayName -eq 'N-Able Agent' -or $_.DisplayName -eq 'N-Able Agent Remediation' } |
    Select-Object -Property DisplayName, UninstallString

    # Check if N-Able Agent is installed
    if ($nable) {
        Write-Host "[Info] N-Able Agent found"
    }
    else {
        Write-Host "[Info] N-Able Agent not found"
        exit 1
    }

    $nable | ForEach-Object {
        $App = $_
        # Uninstall N-Able Agent
        if ($App.UninstallString -match 'msiexec.exe') {
            # Extract the GUID from the UninstallString
            $null = $App.UninstallString -match '{[A-F0-9-]+}'
            $guid = $matches[0]

            Write-Host "[Info] Removing N-Able Agent using msiexec"
            try {
                $Process = $(Start-Process -FilePath "msiexec.exe" -ArgumentList "/x $($guid) /qn /norestart" -Wait -PassThru)
                if ($Process.ExitCode -ne 0 -and $Process.ExitCode -ne 3010) {
                    throw $Process.ExitCode
                }
                if ($Process.ExitCode -eq 3010) {
                    Write-Host "[Info] Restart Required"
                }
            }
            catch {
                Write-Host "[Error] Error removing N-Able Agent. Exit Code: $($Process.ExitCode)"
                exit 1
            }
        }
        elseif ($App.UninstallString -match 'unins000.exe') {
            Write-Host "[Info] Removing N-Able Agent using unins000.exe..."
            try {
                $Process = $(Start-Process -FilePath "$($App.UninstallString)" -ArgumentList "/arp /S /norestart" -Wait -PassThru)
                if ($Process.ExitCode -ne 0 -and $Process.ExitCode -ne 3010) {
                    throw $Process.ExitCode
                }
                if ($Process.ExitCode -eq 3010) {
                    Write-Host "[Info] Restart Required"
                }
            }
            catch {
                Write-Host "[Error] Error removing N-Able Agent. Exit Code: $($Process.ExitCode)"
                exit 1
            }
        }
        else {
            Write-Host "[Error] Unsupported uninstall method found."
            exit 1
        }
    }

    Write-Host "[Info] N-Able Agent successfully removed"
    exit 0
}
end {



}
