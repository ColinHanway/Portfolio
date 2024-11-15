#Requires -Version 5.1

<#
.SYNOPSIS
    Removes Symantec Endpoint Protection from the system.
.DESCRIPTION
    Removes Symantec Endpoint Protection from the system.

    Note: Other Symantec Endpoint Protection related applications will not be removed. This script can be modified to account for them if needed.
      See line 43 for more details
.EXAMPLE
    (No Parameters)

    [Info] Symantec Endpoint Protection found
    [Info] Removing Symantec Endpoint Protection using msiexec
    [Info] Symantec Endpoint Protection successfully removed
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

    # Get UninstallString for Symantec Endpoint Protection from the registry
    $symantec = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' |
    Where-Object { $_.DisplayName -eq 'Symantec Endpoint Protection' } |
    # Replace the line above with additions like below
    # Where-Object { $_.DisplayName -eq 'Symantec Endpoint Protection' -or $_.DisplayName -eq 'Symantec Endpoint Protection Remediation' } |
    Select-Object -Property DisplayName, UninstallString

    # Check if Symantec Endpoint Protection is installed
    if ($symantec) {
        Write-Host "[Info] Symantec Endpoint Protection found"
    }
    else {
        Write-Host "[Info] Symantec Endpoint Protection not found"
        exit 1
    }

    $symantec | ForEach-Object {
        $App = $_
        # Uninstall Symantec Endpoint Protection
        if ($App.UninstallString -match 'msiexec.exe') {
            # Extract the GUID from the UninstallString
            $null = $App.UninstallString -match '{[A-F0-9-]+}'
            $guid = $matches[0]

            Write-Host "[Info] Removing Symantec Endpoint Protection using msiexec"
            try {
                $Process = $(Start-Process -FilePath "msiexec.exe" -ArgumentList "/x $($guid) /qn /norestart" -Wait -PassThru)
                if ($Process.ExitCode -ne 0) {
                    throw $Process.ExitCode
                }
            }
            catch {
                Write-Host "[Error] Error removing Symantec Endpoint Protection. Exit Code: $($Process.ExitCode)"
                exit 1
            }
        }
        elseif ($App.UninstallString -match 'SymantecUninstaller.exe') {
            Write-Host "[Info] Removing Symantec Endpoint Protection using SymantecUninstaller.exe..."
            try {
                $Process = $(Start-Process -FilePath "$($App.UninstallString)" -ArgumentList "/arp /S /norestart" -Wait -PassThru)
                if ($Process.ExitCode -ne 0) {
                    throw $Process.ExitCode
                }
            }
            catch {
                Write-Host "[Error] Error removing Symantec Endpoint Protection. Exit Code: $($Process.ExitCode)"
                exit 1
            }
        }
        else {
            Write-Host "[Error] Unsupported uninstall method found."
            exit 1
        }
    }

    # $SupportAssistClientUI = Get-Process -Name "SupportAssistClientUI" -ErrorAction SilentlyContinue
    # if ($SupportAssistClientUI) {
    #     Write-Host "[Info] SupportAssistClientUI still running and will be stopped"
    #     try {
    #         $SupportAssistClientUI | Stop-Process -Force -Confirm:$false -ErrorAction Stop
    #     }
    #     catch {
    #         Write-Host "[Warn] Failed to stop the SupportAssistClientUI process. Reboot to close process."
    #     }
    # }

    Write-Host "[Info] Symantec Endpoint Protection successfully removed"
    exit 0
}
end {



}
