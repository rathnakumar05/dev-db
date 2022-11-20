## Parser

## Install
- **update** update: `sudo apt update`
- **python** install: `sudo apt install python3`
- **pip** install: `sudo apt install python3-pip`
- **sqlite** install(optional): `sudo apt install sqlite3 `

## App
- `cd  dev-db`
- `pip3 install flask`
- `pip3 install waitress`
- `python3 ./migrate.py` (if db is not present)
- `sudo chmod 777 ./autosetup.sh`
- `./autosetup.sh`
- `sudo systemctl status parser.service` To check status
- `sudo systemctl stop parser.service` To stop
- `sudo systemctl start parser.service` To start
- `sudo systemctl restart parser.service` To restart

## Cron job

- To view cron jobs `crontab -l`
- To edit cron jobs `crontab -e`
- To remove All `crontab -r`

## Commands to add cron jobs
- `(crontab -l ; echo "* * * * * sleep 5 ; /bin/python3 /home/pi/dev-db/parser.py") | crontab -` 
- `(crontab -l ; echo "0 */8 * * * /bin/python3 /home/pi/dev-db/delete.py") | crontab -`

- To remove parser cron jobs only, search for the below lines in the edit mode `crontab -e` and clear it.

- `* * * * * sleep 5 ; /bin/python3 /home/pi/dev-db/parser.py`
- `0 */8 * * * /bin/python3 /home/pi/dev-db/delete.py`

## Note

flask version : 1.0.2
waitress version : 1.4.4