#!/bin/sh

wget https://github.com/hawier-dev/appimages-dl/releases/download/v0.0.1/appimgdl
chmod +x appimgdl
echo "Moving executable to /usr/share/bin/"
sudo mkdir -p /usr/local/bin/
sudo mv appimgdl /usr/local/bin/
echo "Installed"