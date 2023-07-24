param (
    [string]$SOURCE = "models\",
    [string]$DESTINATION = "src/assets/models.json"
)

$paths = Get-ChildItem -Path $SOURCE -Filter "*.skel" -Recurse | ForEach-Object { $_.FullName }
$items = @()

foreach ($path in $paths) {
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($path)
    $name = $filename -replace "_home", ""
    $items += @{
        "name" = $name.Substring(0, 1).ToUpper() + $name.Substring(1)
        "path" = $path
    }
}

$itemsToJson = $items | ConvertTo-Json
'{"assets":' + $itemsToJson + '}' | Out-File $DESTINATION
