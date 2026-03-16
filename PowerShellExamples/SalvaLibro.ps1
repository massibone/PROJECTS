param (
    [string]$Utente,
    [string]$Autore,
    [bool]$LettoTutto,
    [string]$Titolo
)

$percorsoFile = "C:\percorso\del\tuo\file\libri_letti.txt"
$infoLibro = "$Utente | $Autore | Letto tutto: $LettoTutto | Titolo: $Titolo"
Add-Content -Path $percorsoFile -Value $infoLibro
Write-Host "Le informazioni sul libro sono state salvate correttamente."
