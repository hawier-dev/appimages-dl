# AppImages Downloader

A simple application for downloading appimages.

### Automatic installation

```
curl https://raw.githubusercontent.com/hawier-dev/appimages-dl/main/install.sh | bash
```

### Manual installation

Install python packages.

```
python -m pip install typer beautifulsoup4 requests tqdm
```

Download executable.

```
wget https://github.com/hawier-dev/appimages-dl/releases/download/v0.0.2/appimgdl
```

Make it executable by the user.

```
chmod +x appimgdl
```

Move executable to /usr/local/bin

```
sudo mv appimgdl /usr/local/bin
```

### Usage

##### Update repo:

```
appimgdl updaterepo
```

##### Download Appimage:

```
appimgdl get <appimage>
```

##### Remove Appimage:

```
appimgdl remove <appimage>
```

##### List of installed Appimages:

```
appimgdl list
```
