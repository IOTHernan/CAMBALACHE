# powershell_scripts.ps1

function youtubesubs: # Parameter help description
[Parameter(AttributeValues)]
[ParameterType]
$ParameterName)
# Script para descargar subtítulos de YouTube
param (
    [Parameter(Mandatory=$true)]
    [string]$url,

    [string]$outputFile = "subtitles.txt"
)
# Validar que la URL no esté vacía
if ([string]::IsNullOrWhiteSpace($url)) {
    Write-Error "El parámetro de URL es obligatorio."
    exit 1
}
# Validar que el archivo de salida no esté vacío, si lo está asignar "subtitles.txt"
if ([string]::IsNullOrWhiteSpace($outputFile)) {
    $outputFile = "subtitles.txt"
}

# Obtener el contenido de la página
$response = Invoke-WebRequest -Uri $url -UseBasicParsing
$subtitleURL = $response.Links | Where-Object { $_.href -like '*&fmts=1*'} | Select-Object -ExpandProperty href

# Descargar los subtítulos
Invoke-WebRequest -Uri $subtitleURL -OutFile $outputFile

Write-Output "Subtítulos descargados en $outputFile"

function Script1 {
    Write-Output "Este es el Script 1"
}

function Script2 {
    Write-Output "Este es el Script 2"
}

function Script3 {
    Write-Output "Este es el Script 3"
}

param (
    [string]$scriptName
)

switch ($scriptName) {
    "Script1" { Script1 }
    "Script2" { Script2 }
    "Script3" { Script3 }
    default { Write-Output "Script no encontrado" }
}
