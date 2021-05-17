# C-ITS CAM decoder and CAM message generator

## Installations required for LocalHost
### Install DUST Ubuntu 18.04.5LTS
1. Open a new terminal and download this repository: 
- `git clone https://gitlab.ilabt.imec.be/flexible-networking-v2x-team-antwerp/dust-camino-install-essentials.git`
- $ `sudo dpkg -I dust_2.0.0_amd64.deb`
- The DUST Core has been installed.
2. install the DUST Core:
- `cd DUST-CAMINO-INSTALL-essentials`
- $ `sudo dpkg -I dust_2.0.0_amd64.deb`
-  Done! It has been installed.
3. Install the python DUST plugin
- $ `pip3 install pydust_core-2.0.0-cp36-cp36m-linux_x86_64.whl`
- Done! It has been installed.
4. Install the java DUST plugin
- $ `cd dust-java`
- $ `sudo apt-get install openjdk-8-jdk`
- $ `sudo apt install maven`
- $ `cd dust-java`
- $ `mvn package`
- $ `mvn install`
- Done! The java DUST plugin has been installed.


### Install requirements
1. Python 3 or newer  
- `pip3 install gpsd-py3`
- `pip3 install asn1tools`
- `pip3 install watchdog`

### Run the decoder
1. Open a new browser window: and put the following in your URL:
- `python3 main-hybrid-service.py`
2. Please see my manual attached to this project how to use and configure everything.

