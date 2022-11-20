## Parser

## Install
- **update** update: `sudo apt update`
- **python** install: `sudo apt install python3`
- **pip** install: `sudo apt install python3-pip`
- **sqlite** install(optional): `sudo apt install sqlite3 `

## App
- `cd  dev-db`
- `pip3 install flask`
- `python3 ./migrate.py` (if db is not present)
- `sudo chmod 777 ./autosetup.sh`
- `./autosetup.sh`
- `sudo systemctl status parser.service`

## Cron job

- To view cron jobs `crontab -l`
- To edit cron jobs `crontab -e`
- To remove All `crontab -r`

- To remove parser cron jobs only, search for the below lines in the edit mode `crontab -e` and clear it.

- `* * * * * sleep 5 ; /bin/python3 /home/pi/dev-db/parser.py`
- `0 */8 * * * /bin/python3 /home/pi/dev-db/delete.py`