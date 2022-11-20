sudo cp /home/pi/dev-db/parser.service /lib/systemd/system/parser.service

sudo systemctl enable parser.service

sudo systemctl start parser.service

