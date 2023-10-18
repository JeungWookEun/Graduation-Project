
Import-Module C:\PowerGRR-0.12.0\PowerGRR-0.12.0\PowerGRR.psd1 -force;
$GRRCredential = Microsoft.PowerShell.Security\get-credential -UserName admin -Message 'GRR 인증 password 입력중 기다리세요';
Get-GRRHuntResult -HuntId D7AF7B5CC66731DE
_system1 -ShowJSON > C:\PowerGRR-0.12.0\PowerGRR-0.12.0\test1.json
