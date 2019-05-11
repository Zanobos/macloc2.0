# Macloc

> Macloc server and webapp

## Sources

- **webapp** :
    the dedicated web application. 
- **webserver** :
    the complete webserver.

## Development

Check the [instructions](DEVELOP.md)

## Raspberry setup

1) Install 2018-11-13-raspbian-stretch-lite in an ssd with rufus. This image does not have a desktop environment. Follow [these instructions](https://www.raspberrypi.org/documentation/installation/installing-images/) for a detailed guide
2) Create an empty file inside the boot partition of the ssd, for example with the command "touch ssh" in order to enable ssh daemon, as specified by [this guide](https://www.raspberrypi.org/documentation/remote-access/ssh/), paragraph 3
3) Connect with ssh using default username and password **pi/raspberrypi** via command line (unix environment) or putty (windows environment)
4) Create a dedicated user and change default password for user pi for security reason to something secure
```sh
sudo adduser macloc
sudo usermod -aG sudo macloc
passwd
```
5) Logout from user pi and login using user macloc with the password set at point 4
6) Remove ssh access with root account and allow only ssh login (optional)
```sh
mkdir -p ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDo/lqJ5dK+pXu+hzMObW4zD/XiElCRF/5nFqA0WMpbaKA2g1arjwXI+8RJKJANzyWCTApxPkVobH4e0qdOzEK2r4qxp+RyWfDINmpYI/O44ulqbcD6ocowkDAXyLrM/UAWciljutQ1TMbcqNlGI2mSPxonIA158A9XvJ4J+4CgIJn/iHlgO4m0/hz6/NtHyunVcZeaDonCxpjQ5WoazBq/slesMTJiXUR5RgNjH14ylkl3IZzyR/R/gM+uVMFUiqT7uyFQ8a+TsDdxl+3Bga3K//aiDY14XjyAw0dqBh0YHNuzgHJ1+LIIHAuypcCEPV30+T4GHfiveolNXFHuYzrf macloc" > ~/.ssh/authorized_keys/macloc.pub

sudo vim "/etc/ssh/sshd_config"
```
> /etc/ssh/sshd_config
```
PermitRootLogin no
PasswordAuthentication no
```
7) Install needed unix packages
```sh
sudo apt-get -y update
sudo apt-get -y install git vim python3 python3-venv python3-dev supervisor apache2 npm
```
8) Prepare the workspace for backend server:
```sh
cd ~
echo "export FLASK_APP=webserver.py" >> ~/.profile
mkdir workspace
cd workspace
git clone https://github.com/Zanobos/macloc
cd macloc/webserver
python3 -m venv venv
source venv/bin/activate
pip install -r app/doc/requirements.txt
pip install gunicorn
flask db upgrade
```
9) Prepare supervisor to always have a backend server running
```sh
sudo touch /etc/supervisor/conf.d/maclocbe.conf
sudo vim /etc/supervisor/conf.d/maclocbe.conf
```
> /etc/supervisor/conf.d/maclocbe.conf
```
[program:maclocbe]
command=/home/macloc/workspace/macloc/webserver/venv/bin/gunicorn -b 192.168.1.200:5000 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 webserver:app
directory=/home/macloc/workspace/macloc/webserver
user=macloc
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
10) Prepare the hardware for can acquisition. Connect the can controller to the RPI, then
```sh
sudo apt-get install can-utils
sudo vim /boot/config.txt
```
> /boot/config.txt
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
dtoverlay=spi-bcm2835-overlay
```
```sh
sudo reboot
```
Login again inside the raspberry with user macloc
```sh
sudo touch /etc/network/interfaces.d/can0
sudo vim /etc/network/interfaces.d/can0
```
> /etc/network/interfaces.d/can0
```
auto can0
iface can0 can static 
    bitrate 500000
```
```sh
sudo reboot
```
11) Configure apache to serve the front end files
```sh
sudo chown -R macloc /var/www/html/
sudo chgrp -R www-data /var/www/html/
sudo touch /etc/apache2/sites-available/macloc.conf
sudo vim /etc/apache2/sites-available/macloc.conf
```
> /etc/apache2/sites-available/macloc.conf
```
<VirtualHost *:80>
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        ProxyPass /api/socket.io/ ws://192.168.1.200:5000/api/socket.io/
        ProxyPassReverse /api/socket.io/ ws://192.168.1.200:5000/api/socket.io/
        ProxyPass /api/ http://192.168.1.200:5000/api/
        ProxyPassReverse /api/ http://192.168.1.200:5000/api/
</VirtualHost>
```
```sh
sudo a2enmod proxy proxy_http proxy_wstunnel
sudo a2dissite 000-default
sudo a2ensite macloc
sudo systemctl restart apache2
```
12) Set up FE files
```sh
cd ~/workspace/macloc/webapp
cp -R dist/* /var/www/html
```
13) Configure the static IP (and also the gateway ip if internet access is needed)
```sh
sudo vim /etc/dhcpcd.conf
```
> /etc/dhcpcd.conf
```
interface eth0
static ip_address=192.168.1.200/24
static routers=192.168.1.254
static domain_name_servers=192.168.1.254
```