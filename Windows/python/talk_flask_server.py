import json
from datetime import datetime
from flask import Flask, request, make_response
from slack_sdk import WebClient
import os, jsonify
import subprocess
import hashlib
import requests
import pyautogui
import time
import pytz
from apscheduler.schedulers.background import BackgroundScheduler



# Slack 앱 토큰 설정
token = "xoxb-3751783231122-5785231702129-da2yw6KZm0o7tBBJ6H9wH5ek"
app = Flask(__name__)
client = WebClient(token)

# grr_hunt.txt 파일 읽기
try:
    with open("grr_hunt.txt", "r", encoding="utf-8") as file:
        show_delita = file.read()
except UnicodeDecodeError:
    # If the file is not UTF-8 encoded, try another encoding (e.g., ISO-8859-1)
    with open("grr_hunt.txt", "r", encoding="ISO-8859-1") as file:
        show_delita = file.read()


# 현재 요일 반환 함수
def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = '{}({})'.format(date, weekday)
    return result


# 현재 시간 반환 함수
def get_datetime():
    return datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")



# 진행 상황 블록 메시지 생성 함수
def create_progress_block():
    current_datetime = get_datetime()  # 현재 날짜와 시간 가져오기

    # grr_hunt.txt 파일 읽기
    try:
        with open("C:\PowerGRR-0.12.0\PowerGRR-0.12.0\process.txt", "r", encoding="utf-16") as file:
            show_delita = file.read()
    except UnicodeDecodeError:
        # If the file is not UTF-8 encoded, try another encoding (e.g., ISO-8859-1)
        with open("C:\PowerGRR-0.12.0\PowerGRR-0.12.0\process.txt", "r", encoding="ISO-8859-1") as file:
            show_delita = file.read()

    progress_block = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "GRR 시스템 실행중입니다."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*GRR START TIME:* {}\nWINDOWS 내 파일 시스템 내부 및 경로로 점검 진행중".format(current_datetime)
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notifications.png",
                    "alt_text": "calendar thumbnail"
                }
            },
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "진단 세부 내역",
                                "style": {
                                    "bold": True
                                }
                            },
                            {
                                "type": "text",
                                "text": "\n\n"
                            }
                        ]
                    },
                    {
                        "type": "rich_text_preformatted",
                        "border": 0,
                        "elements": [
                            {
                                "type": "text",
                                "text": show_delita  # grr_hunt.txt 파일 내용 출력
                            }
                        ]
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
                        "alt_text": "notifications warning icon"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "예상 시간 약 30분 ~ 1시간 소요 예정\n*결과를 출력하실때 @<GRR_BOT> windows_result 를 입력하여 주세요*"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }
    return progress_block


# 결과 블록 메시지 생성 함수
def create_result_block():
    result_block = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Windows PC GRR 결과:*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Type:*\n[file type]\n*When:*\nAug 10-Aug 13\n*Hours:* 16.0 (2 days)\n*V.T 위험도:*\n [악성유무 및 위험도:star::star::star:]\n*설명:* [어떤 위험?]"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://www.softwarecatalog.co.kr/src/Item/Images/BADX.jpg",
                    "alt_text": "computer thumbnail"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "허용"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "제거"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }
    return result_block


# GRR 시작 블록 메시지 생성 함수
def create_start_block():
    start_block = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "*Windows PC 진단 GRR이 실행되었습니다.*",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:star::star::star:*Runing GRR*:star::star::star:\n*구동시간:* {}_windows PC\n*예상시간 30 ~ 1:30 소요 예정*\n진행사항을 알고싶으면\n /windows_progress을 입력해 주세요".format(get_datetime())
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://blog.kakaocdn.net/dn/vw5kI/btrX2V1UhXb/nwe1Y7uw07dzkLy0bS1u0k/img.jpg",
                    "alt_text": "alt text for image"
                }
            },
            {
                "type": "divider"
            }
        ]
    }
    return start_block

# 백그라운드 작업 함수
def scan_file_and_send_result():
    # JSON 파일 두 개를 읽어옵니다.
    with open(r"C:\PowerGRR-0.12.0\PowerGRR-0.12.0\py_slackbot_test\json_ret\test1.json", "r") as file1, open(r"C:\PowerGRR-0.12.0\PowerGRR-0.12.0\py_slackbot_test\json_ret\test2.json", "r") as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    # 각 파일에서 hash 값을 추출합니다.
    hash_set1 = set(entry["payload"]["hash_entry"]["sha256"] for entry in data1["items"])
    hash_set2 = set(entry["payload"]["hash_entry"]["sha256"] for entry in data2["items"])

    # 두 세트를 비교하여 중복되지 않는 항목을 찾습니다.
    unique_hashes = hash_set1.symmetric_difference(hash_set2)

    # 중복되지 않는 hash 값을 가진 항목을 리스트로 저장합니다.
    unique_entries = []

    # index를 1부터 시작하도록 초기화합니다.
    index = 1

    for entry in data1["items"] + data2["items"]:
        if entry["payload"]["hash_entry"]["sha256"] in unique_hashes:
            sha256 = entry["payload"]["hash_entry"]["sha256"]
            sha1 = entry["payload"]["hash_entry"]["sha1"]
            md5 = entry["payload"]["hash_entry"]["md5"]
            path = entry["payload"]["stat_entry"]["pathspec"]["path"]
            timestamp = entry["timestamp"]
            unique_entry = {
                "index": index,
                "sha256": sha256,
                "sha1": sha1,
                "md5": md5,
                "path": path,
                "timestamp": timestamp
            }
            unique_entries.append(unique_entry)
            # 다음 항목을 위해 index를 증가시킵니다.
            index += 1

    # 중복되지 않는 hash 값을 가진 항목을 JSON 파일로 저장합니다.
    with open(r"C:\PowerGRR-0.12.0\PowerGRR-0.12.0\py_slackbot_test\json_ret\result_grr_data.json", "w", encoding="UTF-16") as output_file:
        json.dump(unique_entries, output_file, indent=4)

    # VT 스캔 및 결과 저장
    api_key = "1222899cb078a1baedc9db0755c86f5ff283d1511ddd5fc33e12fb084724f246"
    result_file_path = r"C:\PowerGRR-0.12.0\PowerGRR-0.12.0\py_slackbot_test\json_ret\result_grr_data.json"

    # VT 스캔 및 결과 저장
    response_list = []
    response_ret = None  # 변수 미리 초기화

    with open(result_file_path, "r", encoding="utf-16") as result_file:
        unique_entries = json.load(result_file)

    if unique_entries:
        entry = unique_entries[0]
        sha256_hash = entry["sha256"]
        print(sha256_hash)
        file_path = entry["path"]
    
        scan_url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"
        headers = {
            "x-apikey": api_key
        }
    
        response = requests.get(scan_url, headers=headers)
    
        if response.status_code == 200:
            scan_result = response.json()
    
            # VT 결과 처리
            file_risk, status_message, formatted_date, formatted_time, vt_link = "", "", "", "", ""
            if scan_result:
                VT_TIME = scan_result["data"]["attributes"]["last_modification_date"]
                korea_timezone = pytz.timezone("Asia/Seoul")
                utc_time = datetime.fromtimestamp(VT_TIME, tz=pytz.UTC)
                korea_time = utc_time.astimezone(korea_timezone)
    
                analysis_results = scan_result["data"]["attributes"]["last_analysis_results"]
    
                total_engines = len(analysis_results)
                malicious_engines = sum(1 for result in analysis_results.values() if result.get("category") == "malicious")
    
                if total_engines > 0:
                    file_risk = f"파일 위험도: {malicious_engines}/{total_engines}"
                else:
                    file_risk = "파일 위험도: 알 수 없음"
    
                formatted_date = korea_time.strftime("%Y-%m-d %H:%M:%S")
    
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-d %H:%M:%S")
    
                file_status = scan_result["data"]["attributes"]["last_analysis_stats"]["harmless"]
                if file_status > 0:
                    status_message = "스캔 결과: 악성 파일일 수 있습니다. 관리자에게 문의하세요."
                else:
                    status_message = "스캔 결과: 안전한 파일입니다."
    
                vt_link = f"VirusTotal 파일 정보 링크: https://www.virustotal.com/gui/file/{sha256_hash}/details"
    
            response_ret = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Windows PC GRR 결과:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*대상 경로*: {file_path}\n*결과 해시*: {sha256_hash}\n*파일 위험도*: {file_risk}\n{status_message}\n*VT 서버 시간*: {formatted_date}\n*작동 시간*: {formatted_time}\n*VT 링크*: {vt_link}"
                        },
                        "accessory": {
                            "type": "image",
                            "image_url": "https://www.softwarecatalog.co.kr/src/Item/Images/BADX.jpg",
                            "alt_text": "computer thumbnail"
                        }
                    },
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_preformatted",
                                "border": 0,
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "설치된 파일들에 대한 V.T 스캔 결과 입니다.\n**여러 스캔 결과가 있을 수 있으므로 조금 기다려주세요**"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
    
    return response_ret
            
    
def grr_art():
    ps_script_path = r"C:\\PowerGRR-0.12.0\\PowerGRR-0.12.0\\ret_auto.ps1"

    try:
        # PowerShell 스크립트 실행
        process = subprocess.Popen(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")




# Slack 명령어 처리 및 응답 함수
def get_answer(text):
    user_text = text.replace(" ", "")

    answer_dict = {
        '/windows_start': create_start_block(),
        '/windows_progress': create_progress_block(),
        '/windows_result': scan_file_and_send_result(),
        'help': '"봇으로 진행하고 싶은 사항을 입력해주세요 \n질문 옵션을 알고싶으시면 <@grr_bot 옵션> 을 검색해주세요"',
        '옵션': '/windows_start : GRR 진단 시작\n/windows_progress : PC 진단 진행사항\n/windows_result : PC 진단 결과',
        '진행중': grr_art()
    }

    if user_text == '' or None:
        return "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."
    elif user_text in answer_dict.keys():
        return answer_dict[user_text]
    elif user_text == '진행사항':
        return create_progress_block()
    else:
        for key in answer_dict.keys():
            if key.find(user_text) != -1:
                return "연관 단어 [" + key + "]에 대한 답변입니다.\n" + answer_dict[key]

        for key in answer_dict.keys():
            if answer_dict[key].find(text[1:]) != -1:
                return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n" + answer_dict[key]

    return text + "은(는) 없는 질문입니다."


# PowerShell 스크립트 실행 및 인증 처리 함수
def execute_ps_script():
    ps_script_path = r"C:\\PowerGRR-0.12.0\\PowerGRR-0.12.0\\grr_auto_powershell_sim.ps1"
    username = "admin"
    password = "park1004"

    try:
        # PowerShell 스크립트 실행
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
        # process.wait(20)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Slack 이벤트 핸들러
def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)

    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:
        try:
            if event_type == 'app_mention':
                if "blocks" in slack_event["event"]:
                    text = slack_event["event"]["blocks"][0]["elements"][0]["elements"][1]["text"]
                    if text and len(text.strip()) >= 0:
                        answer = get_answer(text)
                        if isinstance(answer, dict):  # 메시지 블록 형식인 경우
                            result = client.chat_postMessage(channel=channel, blocks=answer["blocks"])
                        else:
                            result = client.chat_postMessage(channel=channel, text=answer)
            elif event_type == 'message':  # 사용자가 직접 메시지를 보낸 경우 처리
                text = slack_event["event"]["text"]
                if text and len(text.strip()) >= 0:
                    answer = get_answer(text, channel)  # 채널 정보를 함께 전달
                    if isinstance(answer, dict):  # 메시지 블록 형식인 경우
                        result = client.chat_postMessage(channel=channel, blocks=answer["blocks"])
                    else:
                        result = client.chat_postMessage(channel=channel, text=answer)
            return make_response("ok", 200, )
        except IndexError:
            pass



# HTTP POST 요청 처리
@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})



# 사용자 정의 Slack 슬래시 명령 처리
@app.route('/slash/', methods=['POST'])
def hello_slash():
    command = request.form['command']
    text = request.form['text']
    user_id = request.form['user_id']
    channel = request.form['channel_id']  # 채널 ID 가져오기

    if command == '/windows_start':
        # 추가: PowerShell 스크립트 실행 및 인증 메시지 대화 상자 처리 함수 호출
        execute_ps_script()
        answer = create_start_block()  # 봇의 명령어를 호출합니다.
    elif command == '/windows_progress':
        answer = create_progress_block()  # 봇의 명령어를 호출합니다.
        answer = "@grr_bot 진행중"
    elif command == '/windows_result':
        answer = "@GRR BOT /windows_result 를 입력하여 주세요"
    else:
        answer = "지원하지 않는 명령입니다."

    return make_response(answer, 200, {"content_type": "application/json"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
