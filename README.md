# IoTMakerLab
Resources for the IoT Maker Lab.

# Installationsguide IoT Maker Lab
Nachdem das Raspbian Betriebssystem auf eine SD-Karte gebrannt und in den Raspberry Pi eingefügt wurde, wird dieser gestartet. 
* Schritt 1: OS Updaten
Zum Updaten des Betriebssystems die Konsole öffnen und folgende Zeile eingeben und mit Enter ausführen:

        sudo update

* Schritt 2: Repos von Git Hub laden
Anschließend werden die Programme und Dateien für den Workshop aus dem GitHub Repository geladen. Hierfür muss im Terminal folgende Zeile eingegeben werden:


	git clone https://github.com/ITInnovationsManagement/IoTMakerLab /home/pi/Desktop/MakerLab
        
Die lädt die Dateien herunter und legt sie auf dem Desktop im Order MakerLab ab.

* Schritt 3: Installationsdatei ausführen
In den Dateien aus GitHub befindet sich eine Installationsdatei zum Installieren der notwendigen Pakete. Durch die Eingabe folgender Statements wird diese ausgeführt:

	sudo chmod+x /home/pi/Desktop/MakerLab/install.sh
	sudo /home/pi/Desktop/MakerLab/install.sh
	
Bei Problemen bei der Installation müssen die Schritte 5 und 6 ausgeführt werden

* Schritt 4: OS konfigurieren
Zum Konfigurieren des Betriebssystems gibt es ein grafisches Tool welches über das Terminal mit folgender Zeile gestartet werden kann:

	sudo raspi-config
	1. Sprache umschalten über Internalisation
	2. SSH einschalten
	3. Boot in Desktop ermöglichen
	
* Schritt 5:  WLAN konfigurieren
Zur Konfiguration des WLAN muss zunächst folgendes Statement im Terminal ausgeführt werden:
sudo nano /etc/network/interfaces

In der sich öffnenden Datei muss folgendes eingegeben werden:

	auto wlan0
	iface lo inet loopback
	iface eth0 inet dhcp

	allow-hotplug wlan0
	iface wlan0 inet manual
	wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

	iface default inet dhcp
Anschließend wird die Datei durch Strg+O gespeichert und mit Strg+X wieder geschlossen.

Danach müssen die Daten der WLAN-Zugänge definiert werden.
Hierfür muss folgende Zeile im Terminal ausgeführt werden:
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

In der sich öffnenden Datei muss folgendes eingegeben werden:

	network={
		ssid="SSID1"
		psk="PASSWORD"
		key_mgmt=WPA-PSK
	}
	network={
		ssid="SSID2"
       		psk="PASSWORD"
		key_mgmt=WPA-PSK
	}

SSID und PASSWORD müssen entsprechend angepasst werden

FALLS install.sh nicht funktioniert hat:
* Schritt 6: Remotedesktop ermöglichen
sudo apt-get install tightvncserver
sudo apt-get install xrdp

* Schritt 7: Developer Tools installieren
sudo pip install azure
sudo pip install RPi.GPIO

sudo apt-get --assume-yes update
sudo apt-get --assume-yes install freetds-dev freetds-bin
sudo apt-get --assume-yes install python-dev python-pip
sudo pip install pymssql==2.1.1

Sollte hierbei die Fehlemeldung auftreten:
 Cannot import IncompleteRead
Müssen folgende Zeilen ausgeführt werden:
		sudo dpkg -l | grep python-requests
		sudo apt-get remove python-pip
		sudo easy_install pip

