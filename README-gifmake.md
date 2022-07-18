# HI I'M KIEN

# Make gif file
## video 
you can find from deviant art, pixel
https://www.deviantart.com/tag/livewallpaper
## Conver video to gif

to convern video to gif (linux) use ffmpeg 
Befor use ffmped u need to install imagemagick (independent)
Them run command like 
ffmpeg -ss 01 -t 14 -i input.mp4 -vf "fps=10,scale=1024:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
View tutorial 
https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality#556031
http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
https://engineering.giphy.com/how-to-make-gifs-with-ffmpeg/
https://www.baeldung.com/linux/convert-videos-gifs-ffmpeg
https://www.linuxshelltips.com/convert-video-to-gif-linux/


