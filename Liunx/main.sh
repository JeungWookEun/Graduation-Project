#!/bin/bash

linux_server_ip="192.168.246.194"
linux_server_user="plitoo"
api_key="0e221937fd76ae8dcac4c66c8d0c4cdeceb3e609acd045d2f690371ebf6d3960"
webhook_url="https://hooks.slack.com/services/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"

#curl "https://hooks.slack.com/workflows/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"

# SSH로 Linux 접속
ssh_remote() {
  ssh "$linux_server_user"@"$linux_server_ip" "$@"
}

# Filesystem info
filesystem_info=$(ssh_remote "df -h")
filesystems=$(echo "$filesystem_info" | awk 'NR>1 {print $1}')

# C2 Server info
c2_server=$(ssh_remote "find /tmp /var/www/html /conf /spider /spider/Resources /spider/Resources/control_server /config /opt/oilrig /opt -type f -size +100000c")

# Normally Path
nor_path=$(ssh_remote "find / -name bin  -o -path '/home' -o -path '/etc' -o -path '/var' -o -path '/tmp' -o -path '/dev'")

# Network Path
network=$(ssh_remote "netstat -antulp | column -t")

# 파일 이름 시간 저장
current_datetime=$(date +'%Y%m%d_%H%M')

# 파일 내용 비교
send_slack_notification() {
  message="$1"
  filename="./date/$current_datetime.txt"
  diff_directory="./diff_data/$current_datetime"

  if [ -n "$c2_files" ]; then
    malware=$(echo "$c2_files" | head -n 1)
  fi

  if [ ! -d "$diff_directory" ]; then
    mkdir -p "$diff_directory"
  fi

  if [ -f "$filename" ]; then
    diff_output=$(diff -u "$filename" "./date/2023MM_main.txt")
    if [ -n "$diff_output" ]; then
      echo "$diff_output" >> "$diff_directory/$current_datetime.txt"
    fi
  fi

  echo "*Filesystem info*" >> "$filename"
  echo "$message" >> "$filename"
  echo "*C2 Server info*" >> "$filename"
  echo "$c2_server" >> "$filename"
  echo "*Normally Path info*" >> "$filename"
  echo "$nor_path" >> "$filename"
  echo "*Network info*" >> "$filename"
  echo "$network" >> "$filename"

  diff_file="$diff_directory/$current_datetime.txt"
  diff_output=$(diff -u "$filename" "/home/plitoo/GRR_IR_service/linux/date/2023MM_main.txt")

  if [ -n "$diff_output" ]; then
    echo "$diff_output" >> "$diff_file"
  fi

  # 경로에 있는 파일 해쉬로 바꿔서 저장
  hash_output=$(ssh_remote "sha256sum \"$malware\"" | awk '{print $1}')
  hash_filename=$(basename "$malware").hash
  echo "$hash_output" > "./diff_hash/$hash_filename"

  # 바이러스토탈에 업로드 후 확인
  response=$(curl -s "https://www.virustotal.com/vtapi/v2/file/report?apikey=$api_key&resource=$hash_output")
  positives=$(echo "$response" | jq -r '.positives')
  total=$(echo "$response" | jq -r '.total')
  permalink=$(echo "$response" | jq -r '.permalink')
  mal_hash=$(echo "$response" | jq -r '.hash')

  if [[ -z "$positives" ]]; then
    positives="N/A"
  fi

  if [[ -z "$mal_hash" ]]; then
    positives="N/A"
  fi

  if [[ -z "$total" ]]; then
    total="N/A"r
  fi

  if [[ -z "$permalink" ]]; then
    permalink="N/A"
  fi

  echo "Ubuntu 18.04 LTS 결과:" >> "$filename"
  echo "대상 경로: $local_path" >> "$filename"
  echo "결과 해시: $mal_hash" >> "$filename"
  echo "파일 위험도: $positives / $total" >> "$filename"
  echo "VT 링크: $permalink" >> "$filename"
  curl -X POST -H 'Content-type: application/json' --data "$payload" "$webhook_url"
}

# 슬랙에 뜨는거
send_slack_notification "\`\`\`
*Change Info:*\`\`\`"
