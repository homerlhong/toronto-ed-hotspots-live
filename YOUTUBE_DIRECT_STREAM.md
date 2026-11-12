# REVENGERS Global — YouTube Live without OBS

This workflow streams your **real browser-rendered** REVENGERS Global dashboard directly to YouTube with FFmpeg and a gentle, locally generated white-noise audio bed.

**Public dashboard:** https://homerlhong.github.io/toronto-ed-hotspots-live/global.html?broadcast=1

## 1. Enable YouTube Live

Sign in at https://studio.youtube.com/ and open **Create → Go live**. Complete channel verification / live activation if prompted. Create an **Unlisted** test stream first. Copy the stream key **only to your Mac**, never to GitHub, a chat, or a screenshot.

## 2. Install FFmpeg on your Mac

If Homebrew is installed:

```bash
brew install ffmpeg
```

Check that `ffmpeg -encoders` includes `h264_videotoolbox`. Enable **Screen & System Audio Recording** for Terminal or your terminal app under macOS Privacy & Security settings, then restart the terminal if required.

## 3. Store the stream key privately

```bash
mkdir -p "$HOME/.config/revengers"
chmod 700 "$HOME/.config/revengers"
umask 077
read -r -s -p "Paste YouTube stream key (hidden): " YT_KEY; echo
printf '%s' "$YT_KEY" > "$HOME/.config/revengers/youtube-stream-key"
unset YT_KEY
chmod 600 "$HOME/.config/revengers/youtube-stream-key"
```

**Do not publish the stream key.** The local script checks for file mode 600.

## 4. Find the screen capture index

```bash
ffmpeg -f avfoundation -list_devices true -i "" 2>&1
```

Choose the **screen capture** device index, not a camera or microphone. Indices vary by Mac. macOS screen recording permissions are required.

## 5. Start a 10-minute private test

Open the dashboard in Chrome or Safari, use fullscreen, and enable broadcast mode:

https://homerlhong.github.io/toronto-ed-hotspots-live/global.html?broadcast=1

Then from your local repository:

```bash
chmod +x scripts/youtube-direct-stream.sh
REVENGERS_SCREEN_INDEX=1 ./scripts/youtube-direct-stream.sh
```

Change `REVENGERS_SCREEN_INDEX` to the index shown by FFmpeg. The script uses **720p30** and **6 Mbps** by default for a conservative pilot. Press Ctrl+C after 10 minutes. Confirm picture, noise volume, dropped frames and YouTube ingest health in Live Control Room.

## Customize

```bash
REVENGERS_SCREEN_INDEX=1 REVENGERS_VIDEO_BITRATE=4500k REVENGERS_NOISE_VOLUME=0.01 ./scripts/youtube-direct-stream.sh
```

`REVENGERS_NOISE_VOLUME=0` silences the generated noise; increase slowly and monitor with headphones. The audio source is synthetic and royalty-free, but continuous white noise may be unpleasant at high volume.

## Operational boundaries

- The script streams **the selected macOS screen**, not a headless browser. Keep the dashboard visible and prevent sleep.
- YouTube must have Live enabled. FFmpeg does not authenticate your Google account; it uses a stream key issued by YouTube.
- The stream key is included in FFmpeg's process command line and may be visible to local administrators/process inspection. Use a dedicated machine/account and keep local access restricted.
- A running script does not guarantee 24/7 uptime. Add process supervision and health checks only after the private pilot works.
- GitHub Pages serves the dashboard but **cannot transmit YouTube video** by itself.
- The dashboard uses USGS and NASA EONET public feeds. It is not an emergency dispatch service.
