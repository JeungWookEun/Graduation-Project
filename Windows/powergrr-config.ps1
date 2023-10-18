#$GRRUrl = "https://main-grrserver.tld"
$GRRUrl = "http://192.168.47.156:8000"
$GRRIgnoreCertificateErrors = $( if ($GRRUrl -match "test") { $true } )
$GRRClientCertIssuer = $( if ($GRRUrl -match "main") { "certificate issuer" } )
$GRRCredential = Microsoft.PowerShell.Security\get-credential