#!/bin/bash
#assinging arguments
DIR=$1
PowerDIR=$2
COUNT=$(echo $* |wc -w)
if [[ $COUNT -lt 2 ]]
then
   echo "Not enough arguments Please specify directory for installation and PowerAPI Path if already installed"
   exit
fi   
#creating directory for PowerAPI

echo "creating directory for PowerAPI"
if [ -d "$DIR" ];then
   echo "dir exist deleting and creating again"
   rm -Rf $DIR
   mkdir $DIR
else
   echo "dir does not exist creating"
   mkdir $DIR
fi   
#checking for python and installed versions
echo "checking for python and installed versions"
V=$(pip show Python | grep Version | cut -c10-)
echo $V
Version='2.7.13'
if [[ -z "$V" ]]; then
   echo "Install Python Version 2.7.11 hence exiting"
   exit
elif [ "$V" == "$Version" ]; then
   echo "Correct Version installed"
else
   echo "Incorrect Version of Python Installed hence exiting"
   exit
fi

echo "checking for sushy"
A=$(pip show sushy)
echo $A	
if [[ -z "$A" ]]; then
   echo "Sushy not installed. Installing sushy"
   pip install sushy
#exit
else
   echo "Sushy already installed"
fi
 
#checking for yaml
echo "checking for yaml"
A=$(pip show pyyaml)
echo $A	
if [[ -z "$A" ]]; then
   echo "Yaml not installed. Installing Yaml"
   pip install yaml
#exit
else
   echo "Yaml already installed"
fi

#checking for python sdk   
echo "checking for python sdk"
A=$(pip show python-ilorest-library)
echo $A	
if [[ -z "$A" ]]; then
   echo "Python sdk not installed. Please install before you start"
   exit
else
   echo "Correct Version of Python sdk installed"
fi
#Cloning the code for PowerAPI-Redfish Plugin from github
echo "Cloning the code for PowerAPI-Redfish Plugin from github"
RedfishPluginDIR=$DIR/PowerAPI-Redfish
if [ -d "$RedfishPluginDIR" ]; then
   echo "Redfish Plugin already exists deleting it and cloning again"
   rm -Rf $RedfishPluginDIR
   cd $DIR
   git clone https://github.hpe.com/HPC-India/PowerAPI-Redfish.git
   
else
   cd $DIR
   git clone https://github.hpe.com/HPC-India/PowerAPI-Redfish.git
   
fi   

#checking for Existence of PowerAPI code on the system 
echo "checking for Existence of PowerAPI code on the system"
#PowerDIR=/opt/A
if [ -d "$PowerDIR" ]; then
   echo "PowerAPI exists on the system"      
else
   echo "Directory does not exist creating and installing PowerAPI"
   
   PowerAPIdir=$DIR/pwrapi-ref
   echo $PowerAPIdir
   if [ -d "$PowerAPIdir" ] ; then
      echo "PowerAPI dir already existing hence deleting"
      rm -Rf $PowerAPIdir
      cd $DIR
      git clone https://github.com/pwrapi/pwrapi-ref.git
   else
      cd $DIR
      git clone https://github.com/pwrapi/pwrapi-ref.git   
   fi

   if [ -d "$PowerAPIdir" ]; then
      echo "PowerAPI cloned successfully"
      cd $PowerAPIdir
   else
      echo "PowerAPI not cloned successfully hence exiting"
      exit
   fi
   cd $PowerAPIdir
#copying redfish related files from main code to PowerAPI code
   echo "copying redfish related files from main code to PowerAPI code"
   cp $RedfishPluginDIR/lib/plugin/* $PowerAPIdir/src/plugins
   echo "installing PowerAPI"
#Checking python path
   echo "checking python path"
   PyPath=$(which python)
   echo $PyPath   
   ./autogen.sh

   ./configure --prefix=/opt/A --with-python=$PyPath
   make
   make install  
   echo "PowerAPI installed Successfully" 
fi   

