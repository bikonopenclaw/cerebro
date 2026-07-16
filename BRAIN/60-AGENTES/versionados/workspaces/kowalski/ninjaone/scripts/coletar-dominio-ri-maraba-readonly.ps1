<# 
Coleta somente leitura para inventario de dominio via NinjaOne.

Uso recomendado no NinjaOne:
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\coletar-dominio-ri-maraba-readonly.ps1

Saida:
  - Gera JSON em C:\ProgramData\Bikon\NinjaOne\ri-maraba-domain-inventory-YYYYMMDD-HHMMSS.json
  - Imprime no console o caminho do arquivo e um resumo curto.

Seguranca:
  - Nao altera AD, GPO, shares, ACLs ou configuracao local.
  - Nao coleta senhas, hashes, secrets ou conteudo de arquivos.
  - Coleta metadados: usuarios, grupos, computadores, GPOs, shares e permissoes.
#>

[CmdletBinding()]
param(
    [string]$OutputPath = "",
    [int]$MaxUsers = 5000,
    [int]$MaxGroups = 3000,
    [int]$MaxComputers = 5000,
    [switch]$IncludeDisabledUsers,
    [switch]$IncludeAdminShares
)

$ErrorActionPreference = "Continue"
$scriptVersion = "2026-07-15.1"

function New-ResultSection {
    param(
        [string]$Name,
        [scriptblock]$ScriptBlock
    )

    try {
        $value = & $ScriptBlock
        return [ordered]@{
            ok = $true
            name = $Name
            data = $value
            error = $null
        }
    }
    catch {
        return [ordered]@{
            ok = $false
            name = $Name
            data = @()
            error = $_.Exception.Message
        }
    }
}

function Convert-Time {
    param($Value)
    if ($null -eq $Value) { return $null }
    try { return ([datetime]$Value).ToString("o") } catch { return [string]$Value }
}

function Select-AdUserSafe {
    param($User)
    [ordered]@{
        samAccountName = $User.SamAccountName
        name = $User.Name
        displayName = $User.DisplayName
        userPrincipalName = $User.UserPrincipalName
        enabled = $User.Enabled
        lockedOut = $User.LockedOut
        passwordExpired = $User.PasswordExpired
        passwordNeverExpires = $User.PasswordNeverExpires
        passwordLastSet = Convert-Time $User.PasswordLastSet
        lastLogonDate = Convert-Time $User.LastLogonDate
        accountExpirationDate = Convert-Time $User.AccountExpirationDate
        department = $User.Department
        title = $User.Title
        mail = $User.Mail
        description = $User.Description
        distinguishedName = $User.DistinguishedName
        memberOf = @($User.MemberOf)
        whenCreated = Convert-Time $User.WhenCreated
        whenChanged = Convert-Time $User.WhenChanged
    }
}

function Select-AdGroupSafe {
    param($Group)
    [ordered]@{
        samAccountName = $Group.SamAccountName
        name = $Group.Name
        groupCategory = [string]$Group.GroupCategory
        groupScope = [string]$Group.GroupScope
        description = $Group.Description
        managedBy = $Group.ManagedBy
        distinguishedName = $Group.DistinguishedName
        memberCount = @($Group.Members).Count
        whenCreated = Convert-Time $Group.WhenCreated
        whenChanged = Convert-Time $Group.WhenChanged
    }
}

function Select-AdComputerSafe {
    param($Computer)
    [ordered]@{
        name = $Computer.Name
        dnsHostName = $Computer.DNSHostName
        enabled = $Computer.Enabled
        operatingSystem = $Computer.OperatingSystem
        operatingSystemVersion = $Computer.OperatingSystemVersion
        lastLogonDate = Convert-Time $Computer.LastLogonDate
        distinguishedName = $Computer.DistinguishedName
        whenCreated = Convert-Time $Computer.WhenCreated
        whenChanged = Convert-Time $Computer.WhenChanged
    }
}

function Get-ShareInventory {
    $shares = Get-SmbShare | Where-Object {
        $IncludeAdminShares -or ($_.Name -notmatch '^[A-Z]\$$' -and $_.Name -notin @("ADMIN$", "IPC$", "PRINT$"))
    }

    foreach ($share in $shares) {
        $shareAccess = @()
        try {
            $shareAccess = Get-SmbShareAccess -Name $share.Name | ForEach-Object {
                [ordered]@{
                    accountName = $_.AccountName
                    accessControlType = [string]$_.AccessControlType
                    accessRight = [string]$_.AccessRight
                }
            }
        }
        catch {
            $shareAccess = @([ordered]@{ error = $_.Exception.Message })
        }

        $ntfsAcl = @()
        if ($share.Path -and (Test-Path -LiteralPath $share.Path)) {
            try {
                $ntfsAcl = (Get-Acl -LiteralPath $share.Path).Access | ForEach-Object {
                    [ordered]@{
                        identityReference = [string]$_.IdentityReference
                        accessControlType = [string]$_.AccessControlType
                        fileSystemRights = [string]$_.FileSystemRights
                        isInherited = $_.IsInherited
                        inheritanceFlags = [string]$_.InheritanceFlags
                        propagationFlags = [string]$_.PropagationFlags
                    }
                }
            }
            catch {
                $ntfsAcl = @([ordered]@{ error = $_.Exception.Message })
            }
        }

        [ordered]@{
            name = $share.Name
            path = $share.Path
            description = $share.Description
            scopeName = $share.ScopeName
            shareState = [string]$share.ShareState
            folderEnumerationMode = [string]$share.FolderEnumerationMode
            cachingMode = [string]$share.CachingMode
            encryptData = $share.EncryptData
            shareAccess = @($shareAccess)
            ntfsAcl = @($ntfsAcl)
        }
    }
}

function Get-LocalAccessInventory {
    $localUsers = @()
    $localGroups = @()

    if (Get-Command Get-LocalUser -ErrorAction SilentlyContinue) {
        $localUsers = Get-LocalUser | ForEach-Object {
            [ordered]@{
                name = $_.Name
                enabled = $_.Enabled
                lastLogon = Convert-Time $_.LastLogon
                passwordLastSet = Convert-Time $_.PasswordLastSet
                passwordRequired = $_.PasswordRequired
                userMayChangePassword = $_.UserMayChangePassword
                description = $_.Description
            }
        }
    }

    if (Get-Command Get-LocalGroup -ErrorAction SilentlyContinue) {
        $localGroups = Get-LocalGroup | ForEach-Object {
            $groupName = $_.Name
            $members = @()
            try {
                $members = Get-LocalGroupMember -Group $groupName | ForEach-Object {
                    [ordered]@{
                        name = $_.Name
                        objectClass = $_.ObjectClass
                        principalSource = [string]$_.PrincipalSource
                    }
                }
            }
            catch {
                $members = @([ordered]@{ error = $_.Exception.Message })
            }

            [ordered]@{
                name = $groupName
                description = $_.Description
                members = @($members)
            }
        }
    }

    [ordered]@{
        localUsers = @($localUsers)
        localGroups = @($localGroups)
    }
}

function Get-GpoInventory {
    $items = @()
    $links = @()

    if (-not (Get-Module -ListAvailable -Name GroupPolicy)) {
        return [ordered]@{
            available = $false
            reason = "Modulo GroupPolicy nao encontrado neste host."
            gpos = @()
            inheritance = @()
        }
    }

    Import-Module GroupPolicy -ErrorAction Stop

    $items = Get-GPO -All | ForEach-Object {
        [ordered]@{
            id = [string]$_.Id
            displayName = $_.DisplayName
            owner = $_.Owner
            domainName = $_.DomainName
            gpoStatus = [string]$_.GpoStatus
            creationTime = Convert-Time $_.CreationTime
            modificationTime = Convert-Time $_.ModificationTime
            userVersion = $_.UserVersion
            computerVersion = $_.ComputerVersion
            wmiFilter = if ($_.WmiFilter) { [string]$_.WmiFilter.Name } else { $null }
        }
    }

    if (Get-Module -ListAvailable -Name ActiveDirectory) {
        Import-Module ActiveDirectory -ErrorAction SilentlyContinue
        $targets = @()
        try {
            $domain = Get-ADDomain
            $targets += $domain.DistinguishedName
            $targets += (Get-ADOrganizationalUnit -Filter * | Select-Object -ExpandProperty DistinguishedName)
        }
        catch {
            $targets = @()
        }

        foreach ($target in $targets) {
            try {
                $inheritance = Get-GPInheritance -Target $target
                $links += [ordered]@{
                    target = $target
                    gpoInheritanceBlocked = $inheritance.GpoInheritanceBlocked
                    inheritedGpoLinks = @($inheritance.InheritedGpoLinks | ForEach-Object {
                        [ordered]@{
                            displayName = $_.DisplayName
                            enabled = $_.Enabled
                            enforced = $_.Enforced
                            order = $_.Order
                            target = $_.Target
                        }
                    })
                    gpoLinks = @($inheritance.GpoLinks | ForEach-Object {
                        [ordered]@{
                            displayName = $_.DisplayName
                            enabled = $_.Enabled
                            enforced = $_.Enforced
                            order = $_.Order
                            target = $_.Target
                        }
                    })
                }
            }
            catch {
                $links += [ordered]@{
                    target = $target
                    error = $_.Exception.Message
                }
            }
        }
    }

    [ordered]@{
        available = $true
        gpos = @($items)
        inheritance = @($links)
    }
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $baseDir = Join-Path $env:ProgramData "Bikon\NinjaOne"
    New-Item -ItemType Directory -Path $baseDir -Force | Out-Null
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $OutputPath = Join-Path $baseDir "ri-maraba-domain-inventory-$stamp.json"
}
else {
    $parent = Split-Path -Parent $OutputPath
    if ($parent) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
}

$adModuleAvailable = [bool](Get-Module -ListAvailable -Name ActiveDirectory)
if ($adModuleAvailable) {
    Import-Module ActiveDirectory -ErrorAction SilentlyContinue
}

$computerInfo = Get-ComputerInfo -Property CsName, CsDomain, CsDomainRole, OsName, OsVersion, WindowsProductName, WindowsVersion

$result = [ordered]@{
    metadata = [ordered]@{
        script = "coletar-dominio-ri-maraba-readonly.ps1"
        version = $scriptVersion
        readonly = $true
        collectedAt = (Get-Date).ToString("o")
        host = $env:COMPUTERNAME
        userContext = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        outputPath = $OutputPath
        limits = [ordered]@{
            maxUsers = $MaxUsers
            maxGroups = $MaxGroups
            maxComputers = $MaxComputers
            includeDisabledUsers = [bool]$IncludeDisabledUsers
            includeAdminShares = [bool]$IncludeAdminShares
        }
    }
    machine = [ordered]@{
        name = $computerInfo.CsName
        domain = $computerInfo.CsDomain
        domainRole = [string]$computerInfo.CsDomainRole
        osName = $computerInfo.OsName
        osVersion = $computerInfo.OsVersion
        windowsProductName = $computerInfo.WindowsProductName
        windowsVersion = $computerInfo.WindowsVersion
    }
    modules = [ordered]@{
        activeDirectory = $adModuleAvailable
        groupPolicy = [bool](Get-Module -ListAvailable -Name GroupPolicy)
        smbShare = [bool](Get-Command Get-SmbShare -ErrorAction SilentlyContinue)
    }
    sections = [ordered]@{}
}

$result.sections.adDomain = New-ResultSection "adDomain" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    $domain = Get-ADDomain
    $forest = Get-ADForest
    [ordered]@{
        domain = [ordered]@{
            dnsRoot = $domain.DNSRoot
            netBIOSName = $domain.NetBIOSName
            distinguishedName = $domain.DistinguishedName
            domainMode = [string]$domain.DomainMode
            infrastructureMaster = $domain.InfrastructureMaster
            pdcEmulator = $domain.PDCEmulator
            ridMaster = $domain.RIDMaster
        }
        forest = [ordered]@{
            name = $forest.Name
            rootDomain = $forest.RootDomain
            forestMode = [string]$forest.ForestMode
            schemaMaster = $forest.SchemaMaster
            domainNamingMaster = $forest.DomainNamingMaster
        }
    }
}

$result.sections.domainControllers = New-ResultSection "domainControllers" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    Get-ADDomainController -Filter * | ForEach-Object {
        [ordered]@{
            hostName = $_.HostName
            name = $_.Name
            site = $_.Site
            ipv4Address = $_.IPv4Address
            operatingSystem = $_.OperatingSystem
            isGlobalCatalog = $_.IsGlobalCatalog
            isReadOnly = $_.IsReadOnly
            operationMasterRoles = @($_.OperationMasterRoles)
        }
    }
}

$result.sections.passwordPolicy = New-ResultSection "passwordPolicy" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    $default = Get-ADDefaultDomainPasswordPolicy
    $fine = @(Get-ADFineGrainedPasswordPolicy -Filter * -ErrorAction SilentlyContinue)
    [ordered]@{
        defaultDomainPolicy = [ordered]@{
            complexityEnabled = $default.ComplexityEnabled
            lockoutDuration = [string]$default.LockoutDuration
            lockoutObservationWindow = [string]$default.LockoutObservationWindow
            lockoutThreshold = $default.LockoutThreshold
            maxPasswordAge = [string]$default.MaxPasswordAge
            minPasswordAge = [string]$default.MinPasswordAge
            minPasswordLength = $default.MinPasswordLength
            passwordHistoryCount = $default.PasswordHistoryCount
            reversibleEncryptionEnabled = $default.ReversibleEncryptionEnabled
        }
        fineGrainedPolicies = @($fine | ForEach-Object {
            [ordered]@{
                name = $_.Name
                precedence = $_.Precedence
                complexityEnabled = $_.ComplexityEnabled
                lockoutThreshold = $_.LockoutThreshold
                maxPasswordAge = [string]$_.MaxPasswordAge
                minPasswordLength = $_.MinPasswordLength
                appliesTo = @($_.AppliesTo)
            }
        })
    }
}

$result.sections.adUsers = New-ResultSection "adUsers" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    $filter = if ($IncludeDisabledUsers) { "*" } else { "Enabled -eq 'True'" }
    @(Get-ADUser -Filter $filter -ResultSetSize $MaxUsers -Properties DisplayName,Description,Department,Title,Mail,LastLogonDate,PasswordLastSet,PasswordNeverExpires,PasswordExpired,LockedOut,AccountExpirationDate,WhenCreated,WhenChanged,MemberOf | ForEach-Object {
        Select-AdUserSafe $_
    })
}

$result.sections.adGroups = New-ResultSection "adGroups" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    @(Get-ADGroup -Filter * -ResultSetSize $MaxGroups -Properties Description,ManagedBy,Members,WhenCreated,WhenChanged | ForEach-Object {
        Select-AdGroupSafe $_
    })
}

$result.sections.adComputers = New-ResultSection "adComputers" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    @(Get-ADComputer -Filter * -ResultSetSize $MaxComputers -Properties OperatingSystem,OperatingSystemVersion,LastLogonDate,WhenCreated,WhenChanged | ForEach-Object {
        Select-AdComputerSafe $_
    })
}

$result.sections.organizationalUnits = New-ResultSection "organizationalUnits" {
    if (-not $adModuleAvailable) { throw "Modulo ActiveDirectory nao encontrado neste host." }
    @(Get-ADOrganizationalUnit -Filter * -Properties Description,ManagedBy,ProtectedFromAccidentalDeletion,WhenCreated,WhenChanged | ForEach-Object {
        [ordered]@{
            name = $_.Name
            distinguishedName = $_.DistinguishedName
            description = $_.Description
            managedBy = $_.ManagedBy
            protectedFromAccidentalDeletion = $_.ProtectedFromAccidentalDeletion
            whenCreated = Convert-Time $_.WhenCreated
            whenChanged = Convert-Time $_.WhenChanged
        }
    })
}

$result.sections.gpo = New-ResultSection "gpo" {
    Get-GpoInventory
}

$result.sections.sharesAndAcl = New-ResultSection "sharesAndAcl" {
    if (-not (Get-Command Get-SmbShare -ErrorAction SilentlyContinue)) { throw "Cmdlet Get-SmbShare nao encontrado neste host." }
    @(Get-ShareInventory)
}

$result.sections.localAccess = New-ResultSection "localAccess" {
    Get-LocalAccessInventory
}

$json = $result | ConvertTo-Json -Depth 12
Set-Content -LiteralPath $OutputPath -Value $json -Encoding UTF8

$summary = [ordered]@{
    ok = $true
    outputPath = $OutputPath
    host = $result.metadata.host
    domain = $result.machine.domain
    domainRole = $result.machine.domainRole
    activeDirectoryModule = $result.modules.activeDirectory
    groupPolicyModule = $result.modules.groupPolicy
    sectionsOk = @($result.sections.GetEnumerator() | Where-Object { $_.Value.ok } | Select-Object -ExpandProperty Key)
    sectionsError = @($result.sections.GetEnumerator() | Where-Object { -not $_.Value.ok } | ForEach-Object {
        [ordered]@{ section = $_.Key; error = $_.Value.error }
    })
}

Write-Output ($summary | ConvertTo-Json -Depth 6)
