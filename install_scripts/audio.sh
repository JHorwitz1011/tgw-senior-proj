cd ~
git clone https://github.com/Seeed-Projects/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh

sudo pip3 install pyalsaaudio
sudo rpi-update a1658b86485225036eeaea7e0ad4438ed1ce3dd2

sudo reboot now
