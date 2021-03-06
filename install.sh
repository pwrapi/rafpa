#!/bin/bash
#assinging arguments
#DIR=$1
PowerDIR=$1
COUNT=$(echo $* |wc -w)
if [[ $COUNT -lt 1 ]]
then
   echo "Not enough arguments Please specify directory for PowerAPI Path if already installed"
   exit
fi

#checking if PowerAPI is existing on your system
echo "Checking if PowerAPI Present on your system"

if [ -d "$PowerDIR" ];then
   echo "PowerAPI Installed on the System. - Yes"
else
   echo "Incorrect PowerAPI Directory Specified. Please Specify the correct Directory"
   exit
fi

#checking OS Version
echo "Checking OS Version"
OSV=$(lsb_release -si)
echo $OSV
UbOS='Ubuntu'
SlesOS='SUSE LINUX'

if [ "$OSV" == "$UbOS" ]; then
   command="apt-get"
elif [[ $SlesOS == *"$OSV"* ]]; then
   command="zypper"
else
   echo "Check for the OS Version Only SLES and Ubuntu Supported"
   exit
fi

#checking for pip
echo "Checking for pip"

if hash pip 2>/dev/null; then
   echo "pip already installed. - Yes"
else
   echo "pip not installed hence installing"
   $command install python-pip
fi

#checking for python and installed versions
echo "Checking for python and installed versions"
V=$(python -V 2>&1 |cut -d " "  -f 2  |cut -d'.' -f1,2)

if [[ -z "$V" ]]; then
   echo "Python not installed hence exiting"
   exit
fi
q=$(echo $V | awk '{ print ($1 >= 2.7 && $1 < 3 ) ? "true" : "false" }')
#echo $q

if [ "$q" == "true" ]; then
   echo "Correct Version installed - Yes"
else
   echo "Incorrect Version of Python Installed hence exiting Please Install Version Greater than 2.7 and Less than 3.0"
   exit
fi

#checking for sushy
echo "Checking for sushy"
A=$(pip show sushy)
#echo $A	
if [[ -z "$A" ]]; then
   echo "Sushy not installed. Installing sushy"
   pip install sushy
#exit
else
   echo "Sushy already installed - Yes"
fi
 
#checking for yaml
echo "Checking for yaml"
A=$(pip show pyyaml)
#echo $A	
if [[ -z "$A" ]]; then
   echo "Yaml not installed. Installing Yaml"
   pip install pyyaml
#exit
else
   echo "Yaml already installed - Yes"
fi

#checking for python sdk   
echo "Checking for python sdk"
A=$(pip show python-ilorest-library)
#echo $A	
if [[ -z "$A" ]]; then
   echo "Python sdk not installed. Please install Python SDK for In-Band-Communication"
   echo "After installation please place the device .so file in your working directory"
   echo "You can download the so file from the location specfied in the README "
else
   echo "Correct Version of Python sdk installed - Yes"
fi

echo "Installation Completed!!!"


