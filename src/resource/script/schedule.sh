sudo grep -v "* * * * * shivanshu cd /home/shivanshu/COVID/src && export DISPLAY=:0.0 && /home/shivanshu/anaconda3/bin/python3 /home/shivanshu/COVID/src/schedulescript.pyw >> /home/shivanshu/COVID/src/resource/logs/log.txt 2>&1 " /etc/crontab > /home/shivanshu/COVID/src/resource/temp/tmpfile.txt && sudo mv /home/shivanshu/COVID/src/resource/temp/tmpfile.txt /etc/crontab