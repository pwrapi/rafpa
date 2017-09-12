# Intro - RAFPA (Redfish Agent for Power API)

Power API core features are exposed to the various clients looking for Power Management across small or large cluster. A device plugin is developed, in current scenario Redfish plugin, which communicates between Power API and the master node.

Redfish plugin talks to the underlying server which conforms to Redfish Standard via RAFPA.

# Prerequisites and Installation

## Prerequisites 
1)	Power API Code.
The Power API Reference Implementation is already available on GitHub 
https://github.com/pwrapi/pwrapi-ref
Please check the README of this for installation
The redfish Plugin will be the part of this repository
2)	Python Version greater than 2.7.9 and lesser than 3.0.
3)	Pip (package management system used to install and manage software packages written in Python) is available on your system
4)	Sushy (Open Source Software) for talking to Redfish Servers using out of band channel.
5)	Python Ilorest Library for talking to Redfish Servers using in band.
6)	YAML package for reading configuration files

## Installation
1)	Our RAFPA agent is available on GitHub for Installation.
The Code consist of python scripts, yaml files for configuration, RAFPA daemon and Installation script.
2)	The installation script (install.sh) will cater to installation of all the necessary mentioned Prerequisites.
3)	The installation script will install the prerequisites if they are already not available on your system.
4)	For in band communication the library will be installed but for it to work hprest_chif.so file needs to be put in your working directory. This is not a mandatory step if a user does not want in band communication.
5)	Once you run the installation script please check for the installation of all the necessary prerequisites along with code base.

# Configuring the YAML files.

 Our code consists of two main YAML configuration files.
## Device specific yaml file 
This file you can find in the location /Installation_Directory/config/devices.
This file contains the information about object (e.g. – chassis, system) and the Redfish specific details about the same.
To configure you need to create a device file according to sample file kept at the location.\
The sample file consists of some necessary parameters like 
Attribute Name:
Get/set: 
       URI: “This represents the redfish URI”
       attribute: “This represents the attribute in the Redfish json file”
       Script :  “This is the name of the module which needs to be loaded for the specific attribute. The scripts are kept at the location /Installation_Directory/lib/python/scripts”.
Please leverage the sample scripts to create your own script for any other extra attribute if required.
## Location specific yaml file 
This file you can find in the location /Installation_Directory/config/location
This file contains the information about the servers with the IP and credentials.
To configure you need to create a device file according to sample file kept at the location.
You can even automate the creation of this file by creating an automation script using the sample automation script. 

Once the configuration files are ready we can now start our RAFPA agent

# Starting and Stopping RAFPA 

The script to start the RAFPA agent it kept at the location /Installation_Directory/bin.
You have to check all the proxies are disabled on your system as it might interfere with the connection to the server.
The script basically loads all the configuration file, connects to the servers and loads the modules for monitoring and controlling the device.
Starting the agent:
Export the environment variable REDFISH_AGENT_ROOT and give the path to your code base.
export REDFISH_AGENT_ROOT = “/Installation_Directory/”.
Go to the path /CODE_PATH/bin. To start the agent first check the status of the daemon:
To check status type the command- ./proxy status if it says not running then start the daemon with the command - ./proxy start . If the status says running then either you can stop the daemon with the command - ./proxy stop and then start it again. You can also restart the already running daemon with the command - ./proxy restart .
There are various options available to work with Agent.
1)      You Can specify the port on which you want to run the agent - ./proxy start -p <port> . The default port will be 8080 . Incase its already occupied please specify some other port.
2)      You Can also specify if you want to run the agent in foreground - ./proxy -f start . By Default it will run in back ground.
3)      To run with both foreground and port option - ./proxy -f start -p <port>





