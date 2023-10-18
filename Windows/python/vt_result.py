import requests
import hashlib
import datetime
import pytz

slack_webhook_url = "https://hooks.slack.com/services/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"

# VT API 키
api_key = "1222899cb078a1baedc9db0755c86f5ff283d1511ddd5fc33e12fb084724f246"

# 스캔할 파일 경로
file_path = "C:/Nmap/zenmap.exe"

# 파일을 읽어서 SHA-256 해시 계산
with open(file_path, "rb") as f:
    file_content = f.read()
    sha256_hash = hashlib.sha256(file_content).hexdigest()

# VT API 엔드포인트 URL
# upload_url = "https://www.virustotal.com/api/v3/files/upload_url"
scan_url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"

headers = {
    "x-apikey": api_key
}

print("파일 SHA-256 해시:", sha256_hash)

# 스캔 결과
response = requests.get(scan_url, headers=headers)

if response.status_code == 200:
    scan_result = response.json()
    print("안티바이러스 엔진 스캔 결과:")
    for engine, result in scan_result["data"]["attributes"]["last_analysis_results"].items():
        print(f"{engine}: {result['result']}")

    print("\n결과 해시:")
    print(sha256_hash)

    print("\n스캔 일자:")
    VT_TIME=scan_result["data"]["attributes"]["last_modification_date"]

    korea_timezone = pytz.timezone("Asia/Seoul")
    utc_time = datetime.datetime.fromtimestamp(VT_TIME, tz=pytz.UTC)
    korea_time = utc_time.astimezone(korea_timezone)

    # 파일 상태 계산 (악성 파일 수 / 전체 엔진 수)
    analysis_results = scan_result["data"]["attributes"]["last_analysis_results"]
    
    total_engines = len(analysis_results)
    malicious_engines = sum(1 for result in analysis_results.values() if result.get("category") == "malicious")
    
    if total_engines > 0:
        file_risk = f"파일 위험도: {malicious_engines}/{total_engines}"
    else:
        file_risk = "파일 위험도: 알 수 없음"

    # VT 서버 시간 출력
    formatted_date = korea_time.strftime("%Y-%m-%d %H:%M:%S")
    print("대한민국 표준시:", formatted_date)

    # 현재 시간
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # 파일 상태 출력
    file_status = scan_result["data"]["attributes"]["last_analysis_stats"]["harmless"]
    if file_status > 0:
        status_message = "\n스캔 결과: 악성 파일일 수 있습니다. 관리자에게 문의하세요."
        print("\n스캔 결과: 악성 파일일 수 있습니다. 관리자에게 문의하세요.")
    else:
        status_message = "\n스캔 결과: 안전한 파일입니다."
        print("\n스캔 결과: 안전한 파일입니다.")

    # VT 링크 생성
    vt_link = f"VirusTotal 파일 정보 링크: https://www.virustotal.com/gui/file/{sha256_hash}/details"
    #################################################################################    

    # 슬랙 메시지 생성
    slack_message = {
        "text": f"*대상 경로*: {file_path}\n*결과 해시*: {sha256_hash}\n*파일 위험도*: {file_risk}\n{status_message}\n*VT 서버 시간*: {formatted_date}\n*작동 시간*: {formatted_time}\n*VT 링크*: {vt_link}"
    }

    # 슬랙으로 메시지 보내기
    response = requests.post(slack_webhook_url, json=slack_message)

    if response.status_code == 200:
        print("슬랙으로 메시지를 성공적으로 전송했습니다.")
    else:
        print("슬랙 메시지 전송 중 오류 발생:", response.status_code)

else:
    print("스캔 결과를 가져오는 중 에러 발생:", response.status_code,"/", "기존 등록되지 않은 해시입니다.")