$networks = netsh wlan show networks mode=bssid
$networks = $networks | Select-String -Pattern 'SSID|BSSID|Signal|Channel|Radio type'

foreach ($network in $networks) {
    $ssid = ($network | Select-String -Pattern 'SSID:').Line.Split(':')[1].Trim()
    $bssid = ($network | Select-String -Pattern 'BSSID:').Line.Split(':')[1].Trim()
    $signal = ($network | Select-String -Pattern 'Signal:').Line.Split(':')[1].Trim()
    $channel = ($network | Select-String -Pattern 'Channel:').Line.Split(':')[1].Trim()
    $radioType = ($network | Select-String -Pattern 'Radio type:').Line.Split(':')[1].Trim()

    Write-Output "SSID: $ssid"
    Write-Output "BSSID: $bssid"
    Write-Output "Signal: $signal%"
    Write-Output "Channel: $channel"
    Write-Output "Radio type: $radioType"
    Write-Output ""
}