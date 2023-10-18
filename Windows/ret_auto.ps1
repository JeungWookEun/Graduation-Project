# 현재 날짜와 시간을 얻습니다.
$currentTime = Get-Date

# 작업 액션을 생성합니다. 실행할 Python 스크립트 파일을 지정합니다.
$action = New-ScheduledTaskAction -Execute 'python.exe' -Argument 'C:\PowerGRR-0.12.0\PowerGRR-0.12.0\py_slackbot_test\ret_grr.py'

# 작업 트리거를 생성합니다. 현재 실행 시간에서 30분 후에 시작하도록 설정합니다.
$trigger = New-ScheduledTaskTrigger -Once -At ($currentTime.AddMinutes(30))

# 작업을 등록합니다. 작업 이름과 트리거를 지정합니다.
Register-ScheduledTask -TaskName 'grr_ret' -Trigger $trigger -Action $action

# 작업에 설명을 추가합니다.
$task = Get-ScheduledTask -TaskName 'grr_ret'
$task.Description = "grr 결과값 받아오는 작업 실행중"

# 작업 트리거를 수정하여 30분 간격으로 반복하도록 설정합니다.
$trigger.RepetitionInterval = "PT30M"  # 30분 간격
$trigger.RepetitionDuration = "P1D"  # 1일 동안 반복

# 수정된 트리거를 업데이트합니다.
Set-ScheduledTask -TaskName 'grr_ret' -Trigger $trigger

# 4시간 후에 작업을 삭제
Start-Sleep -Seconds (4 * 60 * 60)  # 4시간 대기
Unregister-ScheduledTask -TaskName 'grr_ret' -Confirm:$false  # 작업 삭제
