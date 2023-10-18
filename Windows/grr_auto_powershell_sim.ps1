Import-Module C:\PowerGRR-0.12.0\PowerGRR-0.12.0\PowerGRR.psd1 -force
$GRRCredential = Microsoft.PowerShell.Security\get-credential -UserName admin -Message "GRR 인증 password 입력중 기다리세요"

    #컴퓨터이름 출력
$Client_ComputerName = hostname

    #연동된 client를 모두 보는법(clientid만 출력하게 만듬.)
$ALL_Clientid = (Get-GRRClientIdFromComputerName $Client_ComputerName).Clientid

    #클라이언트ID에 라벨 붙이는법(client host name별)
Set-GRRLabel -ComputerName $Client_ComputerName -Label Park

    #클라이언트 ID를 라벨로 찾는법
$clients = Find-GRRClientByLabel -SearchString Park

    #HUNTING 준비 및 시작
    #프로세스 헌팅 준비 + huntid만 출력 변수에 저장
    #시스템 폴더 헌팅
$Huntid_system1 = New-GRRHunt -HuntDescription "file system path hash save1" -Flow FileFinder -RuleType Label -Label Park -ActionType Hash -Mode ALL_HITS -Path 'C:\WINDOWS\**','C:\Users\**','C:\ProgramData\**', 'C:\$Recycle.Bin\**', 'C:\System Volume Information\**','C:\Temp\**','C:\System Volume Information\**','C:\Intel\**','C:\HNC\**','C:\JungUmdata\**','C:\Program Files (x86)\**'
$JSON_system1 = New-GRRHunt -HuntDescription "file system path hash save1" -Flow FileFinder -RuleType Label -Label Park -ActionType Hash -Mode ALL_HITS -Path 'C:\WINDOWS\**','C:\Users\**','C:\ProgramData\**', 'C:\$Recycle.Bin\**', 'C:\System Volume Information\**','C:\Temp\**','C:\System Volume Information\**','C:\Intel\**','C:\HNC\**','C:\JungUmdata\**','C:\Program Files (x86)\**' -ShowJSON > C:\PowerGRR-0.12.0\PowerGRR-0.12.0\process.txt

$Huntid_system1.hunt_id > huntid.txt

    #GRR헌트 시작
Start-GRRHunt -HuntId $Huntid_system1.hunt_id -ShowJSON

