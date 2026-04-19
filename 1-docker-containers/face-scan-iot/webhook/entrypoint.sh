#!/bin/sh
set -eu

FACE_SCAN_MODE="${FACE_SCAN_MODE:-polling}"

case "$FACE_SCAN_MODE" in
  polling)
    exec python polling_forwarder.py
    ;;
  realtime)
    exec python realtime_webhook_receiver.py
    ;;
  *)
    echo "Unknown FACE_SCAN_MODE: $FACE_SCAN_MODE"
    echo "Allowed values: polling, realtime"
    exit 1
    ;;
esac