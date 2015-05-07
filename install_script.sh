#!/bin/bash

# install web server dependencies
sudo apt-get update
sudo apt-get -y install python python-virtualenv nginx supervisor

# install application (source location in $1)
mkdir /home/vagrant/yaybirds
cp -R $1/yaybirds /home/vagrant/yaybirds
cp $1/requirements.txt /home/vagrant/yaybirds

# create a virtualenv and install dependencies
virtualenv /home/vagrant/yaybirds/venv
/home/vagrant/yaybirds/venv/bin/pip install -r /home/vagrant/yaybirds/requirements.txt

# configure supervisor
sudo cp /vagrant/yaybirds.conf /etc/supervisor/conf.d/
sudo mkdir /var/log/yaybirds
sudo supervisorctl reread
sudo supervisorctl update

# configure nginx
sudo cp /vagrant/yaybirds.nginx /etc/nginx/sites-available/yaybirds
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/yaybirds /etc/nginx/sites-enabled/
sudo service nginx restart

echo Application deployed to http://192.168.10.11/
