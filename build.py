pyinstaller ^
 --onefile ^
 --noconsole ^
 --name "DAVID TV" ^
 --icon assets/icon.ico ^
 --add-data "assets;assets" ^
 --add-data "cache;cache" ^
 --add-data "C:\Program Files\VideoLAN\VLC;vlc" ^
 david_tv.py
