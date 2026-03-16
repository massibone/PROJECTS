# GestioneUtentiCSV.ps1
# Legge un CSV di utenti e genera un report di testo
# Utile per amministratori di sistema e uffici PA

param (
    [string]$InputCSV  = "C:\temp\utenti.csv",
    [string]$OutputFile = "C:\temp\report_utenti.txt"
)

# --- Verifica esistenza file input ---
if (-not (Test-Path $InputCSV)) {
    Write-Host "File non trovato: $InputCSV" -ForegroundColor Red
    exit 1
}

# --- Lettura CSV ---
$utenti = Import-Csv -Path $InputCSV -Delimiter ";"

# --- Intestazione report ---
$report = @()
$report += "=" * 40
$report += "REPORT UTENTI - $(Get-Date -Format 'dd/MM/yyyy HH:mm')"
$report += "=" * 40

# --- Elaborazione righe ---
$contatore = 0
foreach ($utente in $utenti) {
    $contatore++
    $report += "$contatore. $($utente.Cognome) $($utente.Nome) | Ufficio: $($utente.Ufficio) | Email: $($utente.Email)"
}

$report += ""
$report += "Totale utenti: $contatore"

# --- Salvataggio report ---
$report | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "Report generato: $OutputFile" -ForegroundColor Green
```

Il CSV di input atteso ha questa struttura:
```
Nome;Cognome;Ufficio;Email
Mario;Rossi;Protocollo;mario.rossi@comune.it
Anna;Bianchi;Anagrafe;anna.bianchi@comune.it
