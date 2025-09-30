# myAI-ps1.ps1

$question = Read-Host "Hello, welcome to myAI. Ask me any yes or no question."

$response = Get-Random -Minimum 1 -Maximum 21

switch ($response) {
    1 { Write-Output "It is certain!" }
    2 { Write-Output "It is decidedly so." }
    3 { Write-Output "Without a doubt" }
    4 { Write-Output "Yes definitely" }
    5 { Write-Output "You may rely on it" }
    6 { Write-Output "As I see it, yes" }
    7 { Write-Output "Most likely" }
    8 { Write-Output "Outlook good" }
    9 { Write-Output "Yes" }
    10 { Write-Output "Signs point to yes" }
    11 { Write-Output "Reply hazy, try again" }
    12 { Write-Output "Ask again later" }
    13 { Write-Output "Better not tell you" }
    14 { Write-Output "Cannot predict now" }
    15 { Write-Output "Concentrate and ask again" }
    16 { Write-Output "Don't count on it" }
    17 { Write-Output "My reply is no" }
    18 { Write-Output "My sources say no" }
    19 { Write-Output "Outlook not so good" }
    20 { Write-Output "Very doubtful" }
    default { Write-Output "Invalid choice" }
}
