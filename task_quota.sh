#!/bin/bash

# Validasi jumlah argumen
if [ "$#" -ne 5 ]; then
    exit 1
fi

# Ambil parameter
USER=$1
SERVICE=$2
ACTION=$3
USAGE=$4
LIMIT=$5

# Endpoint dan token
TARGET="example.com" # HOST / IPV4
TOKEN=$(jq -r '.apikey' /root/.config/config.json)

# Buat JSON payload
JSON_PAYLOAD=$(jq -n \
  --arg type "bandwidth" \
  --arg user "$USER" \
  --arg service "$SERVICE" \
  --arg action "$ACTION" \
  --arg usage "$USAGE" \
  --arg limit "$LIMIT" \
  '{type: $type, user: $user, service: $service, action: $action, usage: $usage, limit: $limit}')

# Kirim request
response=$(curl -s -w "%{http_code}" -o /dev/null \
  -X POST "http://${TARGET}/callback/notif-service" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$JSON_PAYLOAD")

# Keluar dengan kode 0 jika sukses, 1 jika gagal
[ "$response" = "200" ] && exit 0 || exit 1