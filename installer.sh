echo Version 1.0
echo By NoKodaAddictions, NoKoda

echo ---------Commencing Installation---------
echo Do NOT Turn Off Your Raspberry Pi

echo Installing The Latest Version of Python and PIP...
sudo apt-get install python3
sudo apt-get install python3-pip3

echo Installing Packages and Dependencies...
sudo apt-get install net-tools, git
sudo python3 -m pip install trapi flask flask-login requests

echo Copying Files...
sudo rm -rf /home/pi/RPiC
mkdir /home/pi/RPiC
cp -r ./apps/* /home/pi/RPiC

sudo cp ./installer/rc.local /etc/
sudo chmod +x /etc/rc.local

cp ./installer/rc-local.service /etc/systemmd/system
sudo systemctl enable rc-local
systemctl start rc-local.service

echo Pinging Essential Sites...
ping -c 4 http://worldtimeapi.org

echo Synchronizing Time...
python3 /home/pi/RPiC/sync.py

echo All Done!