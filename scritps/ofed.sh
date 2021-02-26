#!/bin/bash
wget -P /tmp http://www.mellanox.com/page/mlnx_ofed_eula?mtag=linux_sw_drivers&mrequest=downloads&mtype=ofed&mver=MLNX_OFED-4.9-2.2.4.0&mname=MLNX_OFED_LINUX-4.9-2.2.4.0-ubuntu20.04-x86_64.iso
sudo mount /tmp/MLNX_OFED_LINUX-4.9-2.2.4.0-ubuntu20.04-x86_64.iso /mnt/
sudo /mnt//mlnxofedinstall

