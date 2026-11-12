#!/bin/bash
# REVENGERS Global — direct YouTube RTMPS stream (macOS + FFmpeg)
# Screen capture requires macOS Screen Recording permission for Terminal/FFmpeg.
# YouTube stream key stays in a local file, never in this public repository.
set -euo pipefail
command -v ffmpeg >/dev/null || { echo "Install FFmpeg first (e.g. brew install ffmpeg)"; exit 1; }
: "${REVENGERS_STREAM_KEY_FILE:=$HOME/.config/revengers/youtube-stream-key}"
if [[ ! -f "$REVENGERS_STREAM_KEY_FILE" ]]; then
  echo "Missing stream key file: $REVENGERS_STREAM_KEY_FILE"
  echo "Create it locally with permissions 600. Never commit or share your stream key."
  exit 1
fi
if [[ "$(stat -f %Lp "$REVENGERS_STREAM_KEY_FILE")" != "600" ]]; then
  echo "Stream key file must have chmod 600 permissions."
  exit 1
fi
KEY="$(tr -d '\r\n' < "$REVENGERS_STREAM_KEY_FILE")"
[[ -n "$KEY" ]] || { echo "Stream key file is empty"; exit 1; }
# Determine screen device number using: ffmpeg -f avfoundation -list_devices true -i ""
SCREEN_INDEX="${REVENGERS_SCREEN_INDEX:-1}"
FPS="${REVENGERS_FPS:-30}"
VIDEO_BITRATE="${REVENGERS_VIDEO_BITRATE:-6000k}"
AUDIO_VOLUME="${REVENGERS_NOISE_VOLUME:-0.025}"
# For white noise, anoisesrc color=white; low volume avoids harsh listening.
# 1280x720 is a conservative starting point for 24/7 testing.
URL="rtmps://a.rtmps.youtube.com/live2/$KEY"
unset KEY
echo "Starting direct YouTube RTMPS stream. Capture device: $SCREEN_INDEX. Press Ctrl+C to stop."
echo "Open your REVENGERS dashboard fullscreen on the selected screen before streaming."
exec ffmpeg -hide_banner -loglevel warning \
  -thread_queue_size 1024 -f avfoundation -framerate "$FPS" -capture_cursor 0 -i "$SCREEN_INDEX:none" \
  -f lavfi -i "anoisesrc=color=white:amplitude=0.15:sample_rate=48000" \
  -filter_complex "[0:v]scale=1280:720:flags=lanczos,format=yuv420p[v];[1:a]volume=$AUDIO_VOLUME,highpass=f=100,lowpass=f=10000,alimiter=limit=0.7[a]" \
  -map "[v]" -map "[a]" \
  -c:v h264_videotoolbox -b:v "$VIDEO_BITRATE" -maxrate "$VIDEO_BITRATE" -bufsize 12000k \
  -r "$FPS" -g 60 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -ac 2 \
  -f flv "$URL"
