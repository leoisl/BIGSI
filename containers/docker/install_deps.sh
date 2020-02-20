#!/usr/bin/env bash
apt-get update
apt-get install -y parallel wget git python3-pip
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda
/root/miniconda/bin/conda init
rm Miniconda3-latest-Linux-x86_64.sh

/root/miniconda/bin/conda config --add channels bioconda
/root/miniconda/bin/conda config --add channels conda-forge
/root/miniconda/bin/conda install -y mccortex kraken2 bracken sourmash

export BERKELEYDB_DIR=~/usr/local/
export BERKELEY_VERSION=4.8.30
# Download, configure and install BerkeleyDB
wget -P /tmp http://download.oracle.com/berkeley-db/db-"${BERKELEY_VERSION}".tar.gz 
tar -xf /tmp/db-"${BERKELEY_VERSION}".tar.gz -C /tmp
rm -f /tmp/db-"${BERKELEY_VERSION}".tar.gz
cd /tmp/db-"${BERKELEY_VERSION}"/build_unix 
../dist/configure --prefix $BERKELEYDB_DIR && make && make install
pip3 install cython
pip3 install bsddb3