pi@raspberrypi:~ $ cat game_console_pc.log
fatal: unable to access 'https://github.com/rickardlindberg/agdpp.git/': Could not resolve host: github.com
Retrying in 1
fatal: unable to access 'https://github.com/rickardlindberg/agdpp.git/': Could not resolve host: github.com
Retrying in 2
fatal: unable to access 'https://github.com/rickardlindberg/agdpp.git/': Could not resolve host: github.com
Retrying in 5
Already up to date.
pi@raspberrypi:~ $ cat game_console_pc.sh 
#!/usr/bin/env bash

exec > /home/pi/game_console_pc.log

exec 2>&1

cd /home/pi/agdpp

for retry in 1 2 5 10 giveup; do
	if [ $retry = giveup ]; then
		echo giving up
		break
	elif git pull --ff-only; then
		break
	else
		echo Retrying in $retry
		sleep $retry
	fi
done

python3 startup.py
pi@raspberrypi:~ $ cat /etc/xdg/autostart/
game_console_start.desktop  pulseaudio.desktop
lxpolkit.desktop            xcompmgr.desktop
pprompt.desktop             xdg-user-dirs.desktop
print-applet.desktop        
pi@raspberrypi:~ $ cat /etc/xdg/autostart/game_console_start.desktop 
[Desktop Entry]
Name=Game console start
Exec=/home/pi/game_console_pc.sh
