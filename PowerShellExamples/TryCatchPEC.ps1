# TryCatchPEC.ps1
# Esempio di gestione errori con try/catch
# Verifica e log di connessione a server PEC/SMTP

param (
    [string]$Server     = "smtp.pec.comune.it",
    [int]   $Porta      = 465,
    [string]$LogFile    = "C:\temp\log_connessione.txt"
)

function Write-Log {
    param([string]$Messaggio, [string]$Livello = "INFO")
    $riga = "$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss') [$Livello] $Messaggio"
    Add-Content -Path $LogFile -Value $riga
    $colore = if ($Livello -eq "ERRORE") { "Red" } else { "Green" }
    Write-Host $riga -ForegroundColor $colore
}

try {
    Write-Log "Tentativo di connessione a $Server sulla porta $Porta"

    # Test connessione TCP al server
    $connessione = New-Object System.Net.Sockets.TcpClient
    $connessione.Connect($Server, $Porta)

    if ($connessione.Connected) {
        Write-Log "Connessione riuscita a $Server : $Porta"
        $connessione.Close()
    }
}
catch [System.Net.Sockets.SocketException] {
    Write-Log "Errore di rete: impossibile raggiungere $Server : $Porta" "ERRORE"
}
catch [System.UnauthorizedAccessException] {
    Write-Log "Accesso negato durante la scrittura del log" "ERRORE"
}
catch {
    # catch generico — cattura qualsiasi altro errore imprevisto
    Write-Log "Errore imprevisto: $($_.Exception.Message)" "ERRORE"
}
finally {
    # finally viene eseguito SEMPRE, con o senza errori
    Write-Log "Verifica completata."
}
