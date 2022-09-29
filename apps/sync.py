import trapi
import os

t = trapi.API(trapi.timezones.AMERICA.NEW_YORK)
t.update()

os.system(f"""
sudo timedatectl set-ntp false
sudo timedatectl set-time {t.date}
sudo timedatectl set-time {t.time.split(".")[0]}
sudo timedatectl set-ntp true

echo Updated Time

sudo timedatectl status
""")