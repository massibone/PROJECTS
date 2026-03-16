# ImportModuleReport.ps1
# Esempio di Import-Module con modulo custom riutilizzabile
# Mmodulo condiviso per funzioni di log e report

# --- File: ModuloPA.psm1 (da salvare separato) ---
# Import-Module .\ModuloPA.psm1

function Write-Log {
    param(
        [string]$Messaggio,
        [string]$LogFile  = "C:\temp\pa_log.txt",
        [string]$Livello  = "INFO"
    )
    $riga = "$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss') [$Livello] $Messaggio"
    Add-Content -Path $LogFile -Value $riga
    $colore = switch ($Livello) {
        "INFO"    { "Cyan" }
        "OK"      { "Green" }
        "ERRORE"  { "Red" }
        default   { "White" }
    }
    Write-Host $riga -ForegroundColor $colore
}

function New-ReportPA {
    param(
        [string]$Titolo,
        [string[]]$Righe,
        [string]$OutputFile = "C:\temp\report_pa.txt"
    )
    $separatore = "=" * 50
    $contenuto  = @()
    $contenuto += $separatore
    $contenuto += "$Titolo - $(Get-Date -Format 'dd/MM/yyyy HH:mm')"
    $contenuto += $separatore
    $contenuto += $Righe
    $contenuto += ""
    $contenuto += "Righe elaborate: $($Righe.Count)"
    $contenuto | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "Report salvato: $OutputFile" -ForegroundColor Green
}

# Esporta le funzioni del modulo — obbligatorio nel .psm1
Export-ModuleMember -Function Write-Log, New-ReportPA
