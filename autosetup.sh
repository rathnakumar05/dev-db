(crontab -l ; echo "* * * * * sleep 5 ; /bin/python3 /home/pi/dev-db/parser.py") | crontab -
(crontab -l ; echo "0 */8 * * * /bin/python3 /home/pi/dev-db/delete.py") | crontab -

sudo cp /home/pi/dev-db/parser.service /lib/system/systemd/parser.service

sudo systemctl enable parser.service

sudo systemctl start parser.service

