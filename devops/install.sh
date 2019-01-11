

sudo add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install language-pack-en -y
apt-get install python3.6 -y
apt-get install git -y
apt-get install screen mc -y
apt-get install python-pip -y
apt-get install python-pip python-dev libmysqlclient-dev -y
#apt-get install mysql-server



vi /etc/default/locale
#add
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8

update-locale


iptables -L
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 5005 -j ACCEPT

ufw allow 22
ufw allow 5000
ufw allow 5005
ufw allow 3306
ufw allow 22/tcp
ufw status
ufw allow 5000/tcp
lsof -i :5000
ufw enable


cd /tmp
curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
bash Anaconda3-5.0.1-Linux-x86_64.sh

sudo mkdir /usr/application
sudo chown tothmiklos /usr/application/
cd /usr/application/

git clone https://mike576@github.com/mike576/btcpred
conda create --name cryptopredenv --file btcpred/requirements.txt

#if needed:
#conda install -c conda-forge tweepy


source activate cryptopredenv
pip install stockstats
pip install matplotlib
pip install tweepy
pip install mysqlclient

#source activate tw-mining36


#!/bin/bash
echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-9-0; then
  # The 16.04 installer works with 16.10.
  curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
  dpkg -i ./cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
  apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
  apt-get update
  apt-get install cuda-9-0 -y
fi
# Enable persistence mode
nvidia-smi -pm 1



source activate cryptopredenv

pip install tensorflow-gpu
pip install keras
pip install matplotlib
