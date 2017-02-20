#!/bin/bash
	
# Remotedesktop ermöglichen
sudo apt-get install tightvncserver
sudo apt-get install xrdp

# Developer Tools installieren
sudo pip install azure
sudo pip install RPi.GPIO

sudo apt-get --assume-yes update
sudo apt-get --assume-yes install freetds-dev freetds-bin
sudo apt-get --assume-yes install python-dev python-pip
sudo apt-get remove python-pip
			
sudo easy_install pip
sudo pip install pymssql==2.1.1
