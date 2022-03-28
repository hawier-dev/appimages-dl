#!/bin/sh

wget https://github.com/hawier-dev/appimages-dl/releases/download/v0.0.1/appimgdl
chmod +x appimgdl
mv appimgdl ~/.local/bin/
echo "Installed"