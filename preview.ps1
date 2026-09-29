$SaveFileDialog1_FileOk = {
}
$Label3_Click = {
}
$Form1_Load = {
}
$Label2_Click = {
}
$Label1_Click = {
}
$Button1_Click = {
}
Add-Type -AssemblyName PresentationFramework

$xamlPath = Join-Path $PSScriptRoot "form.xaml"
$xaml = Get-Content -Path $xamlPath -Raw

# El visor no necesita los eventos que pyRevit conecta desde Python.
$xaml = $xaml -replace '\s+Click="[^"]+"', ''

$reader = New-Object System.Xml.XmlNodeReader ([xml]$xaml)
$window = [Windows.Markup.XamlReader]::Load($reader)

$collectionsList = $window.FindName("collections_list")
$acceptButton = $window.FindName("accept_button")
$cancelButton = $window.FindName("cancel_button")

$collectionsList.ItemsSource = @(
    [pscustomobject]@{ Name = "Arquitectura" }
    [pscustomobject]@{ Name = "Estructura" }
    [pscustomobject]@{ Name = "Instalaciones" }
    [pscustomobject]@{ Name = "MEP" }
)

$acceptButton.Add_Click({ $window.Close() })
$cancelButton.Add_Click({ $window.Close() })

$window.ShowDialog() | Out-Null