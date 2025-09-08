#!/bin/bash

curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/youtube-dl
chmod a+rx /usr/local/bin/youtube-dl


cd /app
youtube-dl -f 'bestaudio[ext=m4a]' $1
mv ./*.m4a ./audio