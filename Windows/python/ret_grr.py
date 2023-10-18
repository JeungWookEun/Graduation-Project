import subprocess
import pyautogui
import time

with open("C:\\PowerGRR-0.12.0\\PowerGRR-0.12.0\\huntid.txt", "r",encoding="UTF-16") as i:
    huntid = i.read()

# PowerShell 스크립트를 생성하고 파일로 저장
ps_script = f"""
Import-Module C:\\PowerGRR-0.12.0\\PowerGRR-0.12.0\\PowerGRR.psd1 -force;
$GRRCredential = Microsoft.PowerShell.Security\\get-credential -UserName admin -Message 'GRR 인증 password 입력중 기다리세요';
Get-GRRHuntResult -HuntId {huntid}_system1 -ShowJSON > C:\PowerGRR-0.12.0\PowerGRR-0.12.0\py_slackbot_test\json_ret\\test2.json
"""

# 스크립트를 파일로 저장
with open("C:\\PowerGRR-0.12.0\\PowerGRR-0.12.0\\ret_grr.ps1", "w") as script_file:
    script_file.write(ps_script)

# PowerShell 스크립트 실행
ps_script_path = "C:\\PowerGRR-0.12.0\\PowerGRR-0.12.0\\ret_grr.ps1"
username = "admin"
password = "park1004"

process = subprocess.Popen(
    ['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_script_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 인증 대화 상자가 나타날 때까지 대기
time.sleep(1)  # 필요에 따라 대기 시간을 조정합니다.
# ID 입력
pyautogui.write(username)  # ID 입력
pyautogui.press('tab')  # 탭 키로 비밀번호 입력 필드로 이동
pyautogui.write(password)  # 비밀번호 입력
pyautogui.press('enter')  # Enter 키로 로그인 또는 확인
time.sleep(0.5)
pyautogui.write(password)  # 비밀번호 입력
pyautogui.press('enter')
