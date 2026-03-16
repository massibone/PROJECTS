# Importa il modulo locale PA e lo usa

Import-Module .\ModuloPA.psm1 -Force

# Uso di Write-Log dal modulo
Write-Log "Avvio elaborazione pratiche" -Livello "INFO"

# Dati di esempio (in produzione verrebbero da Import-Csv)
$pratiche = @(
    "Pratica 001 - Ufficio Anagrafe - Completata",
    "Pratica 002 - Ufficio Protocollo - In attesa",
    "Pratica 003 - Ufficio Tributi - Completata"
)

# Genera report con funzione del modulo
New-ReportPA -Titolo "REPORT PRATICHE GIORNALIERO" -Righe $pratiche

Write-Log "Elaborazione completata" -Livello "OK"
```

