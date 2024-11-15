$regPath = "HKLM:\Software\Google\GCPW"
$name = "domains_allowed_to_login"
$value = "$env:computername, alpha.local, alphamediausa.com"

if (!(Test-Path $regPath)) {
    New-item -Path $regPath -Force | Out-Null
    New-ItemProperty -Path $regPath -Name $name -Value $value -PropertyType String -Force
}
else {
    New-ItemProperty -Path $regPath -Name $name -Value $value -PropertyType String -Force
}
