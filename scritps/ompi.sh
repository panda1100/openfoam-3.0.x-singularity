#!/bin/bash
wget -P /tmp wget https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2
tar -x -f openmpi-2.1.1.tar.bz2 -C /tmp
cd /tmp/openmpi-2.1.1
CC=gcc CXX=g++ F77=gfortran F90=gfortran FC=gfortran ./configure --prefix=/usr/local/openmpi --disable-getpwuid --enable-orterun-prefix-by-default --with-verbs --without-cuda
cd -
/usr/local/openmpi/bin/ompi_info --param btl openib --level 9
