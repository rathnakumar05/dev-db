sudo cp /home/pi/dev-db/parser.service /lib/system/systemd/parser.service

sudo systemctl enable parser.service

sudo systemctl start parser.service

