Write-Output  "
 __      ___         _               ___     _      ___ _           _           
 \ \    / (_)_ _  __| |_____ __ ____| _ \_ _(___ __/ __| |_  ___ __| |_____ _ _ 
  \ \/\/ /| | ' \/ _` / _ \ V  V (_-|  _| '_| \ V | (__| ' \/ -_/ _| / / -_| '_|
   \_/\_/ |_|_||_\__,_\___/\_/\_//__|_| |_| |_|\_/ \___|_||_\___\__|_\_\___|_|  
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
  Get-Service | Where-Object { $_.Status -eq "Running" }
}


GetSystemInfo
GetEnvironmentVariables
GetUserInfo
GetNetworkInfo
GetTaskInfo