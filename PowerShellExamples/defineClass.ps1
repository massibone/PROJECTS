class Human {
    [String]$name = 'homo sapiens'
    [Int]$height = 5

    eat() {
        Write-Host $this.name 'is eating now'
    }
}

# istanza con sintassi moderna
$john = [Human]::new()

# oppure con New-Object
$prateek = New-Object Human
