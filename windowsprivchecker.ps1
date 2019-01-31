$art = "
 _       ___           __                      ____       _          ________              __            
| |     / (_)___  ____/ /___ _      _______   / __ \_____(_)   __   / ____/ /_  ___  _____/ /_____  _____
| | /| / / / __ \/ __  / __ \ | /| / / ___/  / /_/ / ___/ / | / /  / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
| |/ |/ / / / / / /_/ / /_/ / |/ |/ (__  )  / ____/ /  / /| |/ /  / /___/ / / /  __/ /__/ ,< /  __/ /    
|__/|__/_/_/ /_/\__,_/\____/|__/|__/____/  /_/   /_/  /_/ |___/   \____/_/ /_/\___/\___/_/|_|\___/_/          
                                                                                    By 0xc0ffeeadd1c7`r`n"

function GetSystemInfo {
  
  Write-Output "[*] System Info"
 
  systeminfo /fo csv | ConvertFrom-Csv | select OS*, System*, Domain, Hotfix* | Format-List 
  
} 

function GetEnvironmentVariables {

  Write-Output "[*] Environment Variables`r`n"

  $hostname = $env:COMPUTERNAME
  $username = $env:USERNAME
  $path = $env:Path
  $tempdir = $env:TEMP
  $session_name = $env:SESSIONNAME

  Write-Output "HOSTNAME`t`t`t: $hostname`r`nUSERNAME`t`t`t: $username`r`nPATH`t`t`t`t: $path`r`nTEMP`t`t`t`t: $tempdir`r`nSESSIONNAME`t`t`t: $session_name`r`n"

}

function GetUserInfo {

  #declare array of standard/default Windows user accounts - expand this later for RDP/Telnet users and other random junk
  $default_accounts = @("DefaultAccount", "Guest", "WDAGUtilityAccount", "defaultuser0", "HelpAssistant", "HomeGroupUser$")
  
  Write-Output "[*] Local Users`r`n"
  $localusers = Get-LocalUser
  Write-Output "$localusers`r`n"

  $localusers = Get-LocalUser | Where-Object { $_.Name -notin $default_accounts }

  forEach ($user in $localusers)
  {
    Write-Output "[*] Information for user: `"$user`"`r`n"
    net user $user.Name
  }

  Write-Output "[*] Local Groups`r`n"
  Get-LocalGroup
  
}

function GetNetworkInfo {

  Write-Output "[*] Network Information`r`n"
  ipconfig /all
  route print
  
  Write-Output "[*] Reachable Entries From ARP Table `r`n"
  Get-NetNeighbor -State Reachable | select Name,AddressFamily,InterfaceAlias,IPAddress,LinkLayerAddress,State | Format-Table # Show reachable entries from ARP table
 
  Write-Output "[*] Socket Table`r`n" 
  Get-NetTCPConnection -State Listen,Established,TimeWait | select LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess | Format-Table #Show socket table - "Syn Sent" and "Closing" will not be displayed

  Write-Output "[*] Firewall Configuration`r`n"
  netsh advfirewall show currentprofile #if not feeling lazy could use different implementations for OS versions before/after NT 6.0 (netsh advfirewall)
}

function GetTaskInfo {
  
  Write-Output "[*] Scheduled Tasks`r`n"
  Get-ScheduledTask

  Write-Output "[*] Running Services`r`n"
  Get-Service | Where-Object { $_.Status -eq "Running" } | Format-Table
}

function GetPasswordFiles {
  
  Write-Output "[*] Files containing potential passwords`r`n"

  $password_files = @("sysprep.inf", "sysprep.xml", "Unattended.xml
", "Unattended.xml", "Services.xml", "ScheduledTassk.xml", "Printers.xml", "Drives.xml", "DataSources.xml", "groups.xml")

  $file_extensions = @("*.txt", "*.php", "*.conf", "*.py", "*.ps1", "*.conf", "*.config", "*.xml", "*.ini")

  Get-ChildItem -Path C:\Users -Recurse -Force -ErrorAction SilentlyContinue -Include $file_extensions  | Select-String -pattern "password" | select Path | Get-Unique
 
}

function GetRegistryItems {

  Write-Output "[*] `"AlwaysInstallElevated Registry Values`"`r`n"

  $reg_key = ":\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated"

  if ((Test-Path ("HKLM" + $reg_key)) -and (Test-Path ("HKCU" + $reg_key)))
  {
    $hklm_key = Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Installer" -Name "AlwaysInstallElevated"
    $hkcu_key = Get-ItemProperty -Path "HKCU:\SOFTWARE\Policies\Microsoft\Windows\Installer" -Name "AlwaysInstallElevated"

    if ($hklm_key.Name -eq 1 -and $hkcu_key.Name -eq 1)
    {
      Write-Output "[+] SYSTEM Privilege Escalation Found - MSI package installation : http://www.greyhathacker.net/?p=185`r`n"
    }
  } 
}

function ExploitSuggester {

  #include rudimentary cross-check for hotfixes and OS version against list of known KBs
}


Write-Host $art -ForegroundColor Yellow
Write-Host "[*] Starting Enumeration. This can take some time..." -ForegroundColor Green
Write-Host "[+] Getting System info..." -ForegroundColor Green
GetSystemInfo
Write-Host "[+] Getting Environment Variables..." -ForegroundColor Green
GetEnvironmentVariables
Write-Host "[+] Getting User info..." -ForegroundColor Green
GetUserInfo
Write-Host "[+] Getting Network info..." -ForegroundColor Green
GetNetworkInfo
Write-Host "[+] Getting Scheduled Tasks..." -ForegroundColor Green
GetTaskInfo
Write-Host "[+] Searching Filesystem for passwords..." -ForegroundColor Green
GetPasswordFiles
Write-Host "[+] Searching Registry..." -ForegroundColor Green
GetRegistryItems