#!/bin/sh
curl https://bootstrap.pypa.io/get-pip.py | python
python -m pip install -r https://raw.githubusercontent.com/hawier-dev/appimages-dl/main/requirements.txt
wget https://github.com/hawier-dev/appimages-dl/releases/download/v0.0.1/appimgdl
chmod +x appimgdl
echo "Moving executable to /usr/local/bin/"
sudo mkdir -p /usr/local/bin/
sudo mv appimgdl /usr/local/bin/
echo "Installed"