#yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o "kave_voice_raw.mp4" "https://www.youtube.com/watch?v=vEeTqf6PgwI"
# dl with idm
ffmpeg -i kave_voice_raw.mp4 -ar 16000 -ac 1 kave_voice_clean.wav

ffmpeg -i kave_voice_clean.wav -f segment -segment_time 20 -c copy voice/kave_voice_%03d.wav
