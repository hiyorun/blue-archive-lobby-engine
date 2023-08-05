param (
    [string]$SOURCE = 'models/',
    [string]$DESTINATION = 'src/assets/models.json'
)

$paths = Get-ChildItem -Path $SOURCE -Filter "*.skel" -Recurse
$items = @()

foreach ($path in $paths) {
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($path)
    $name = $filename -replace '_home', ''
    $item = @{
        name = $name.Substring(0,1).ToUpper() + $name.Substring(1)
        path = $path.FullName
    }
    $items += $item
}

# Sort the items array by the "name" property before converting to JSON
$sortedItems = $items | Sort-Object -Property name

$itemsToJson = $sortedItems | ConvertTo-Json -Compress
echo $itemsToJson | Out-File -FilePath $DESTINATION
