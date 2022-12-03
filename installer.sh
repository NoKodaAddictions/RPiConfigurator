#Installer Script using URM-API v1.2
#Requires install to /home/pi/ folder
#Also requires installer.py file

echo Version 1.0
echo By NoKodaAddictions, NoKoda

echo ---------Commencing Dependency Installation---------
echo Do NOT Turn Off Your Raspberry Pi

echo Installing The Latest Version of Python and PIP...
sudo apt-get install python3
sudo apt-get install python3-pip3

echo Installing Packages and Dependencies...
sudo apt-get install net-tools, git, ntp, ntpdate
sudo python3 -m pip install trapi flask flask-login requests, urmapi

echo Installing Files via URM-API...
python3 installer.py

echo Modifying System Settings...
sudo chmod +x /etc/rc.local

echo Pinging Essential Sites...
ping -c 4 http://worldtimeapi.org

echo Synchronizing Time...
python3 /home/pi/RPiConfigurator/sync.py

echo All Done!