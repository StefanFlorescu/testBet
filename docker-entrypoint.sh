#!/usr/bin/env bash

set -euo pipefail

/usr/bin/supervisord --configuration /etc/supervisord.conf &
supervisor_pid=$!

cleanup() {
    kill -TERM "${supervisor_pid}" 2>/dev/null || true
    wait "${supervisor_pid}" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

sleep 2
"$@"
