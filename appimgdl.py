
import os
from pathlib import Path
from tqdm import tqdm
import typer
import requests
from bs4 import BeautifulSoup
import platform

app = typer.Typer(help="Appimages downloader.")
page = requests.get("https://appimage.github.io/apps/")
soup = BeautifulSoup(page.content, "html.parser")
download_directory = str(Path.home()) + "/Applications"
desktop_directory = str(Path.home()) + "/.local/share/applications/appimages"
icons_path = str(Path.home()) + "/.icons"
program_list_directory = str(Path.home()) + "/.var/appimgdl"
program_list_file = str(Path.home()) + "/.var/appimgdl/appimages.txt"


def create_desktop_file(appname: str, path: str):
    if not os.path.exists(desktop_directory):
        os.makedirs(desktop_directory)
    desktop_file_path = f"{desktop_directory}/{appname.lower()}".rstrip()
    desktop_file = f"""[Desktop Entry]
Name={appname.rstrip()}
Exec={path.rstrip()}
Icon={appname.lower().rstrip()}
Type=Application"""
    with open(f"{desktop_file_path}.desktop", "w") as f:
        print(f"Creating desktop file in {desktop_directory}")
        f.write(desktop_file)
    return


def download(download_link: str, asset, app):
    # Downloading appimage
    print(f"Downloading: {asset.text}")
    appimage_path = f"{download_directory}/{asset.text}"
    response = requests.get(
        f"{download_link}/{asset.text}", stream=True)
    # Appimage size
    total = int(response.headers.get(
        'content-length', 0))
    # Progress bar
    with open(appimage_path, 'wb') as file, tqdm(
        desc=asset.text,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    os.chmod(appimage_path, 0o775)

    # Create desktop file
    create_desktop_file(
        appname=app, path=appimage_path)
    return


@app.command()
def get(appimage: str):
    """
    Download appimage.
    """
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    if not os.path.exists(icons_path):
        os.makedirs(icons_path)
    if not os.path.exists(program_list_directory):
        os.makedirs(program_list_directory)
        if not os.path.exists(program_list_file):
            updaterepo()
    print(f"Searching for appimage: {appimage}")
    with open(program_list_file, 'r') as f:
        for app in f:
            if appimage == app.lower().rstrip():
                print(f"Found: {app}")
                try:
                    download_page = requests.get(
                        ("https://appimage.github.io/"+app).rstrip())
                    soup = BeautifulSoup(download_page.content, "html.parser")
                    links = soup.find('a', attrs={"class": "button green"})
                    tag_link = links.get('href') + '/latest'
                except AttributeError:
                    print("Error: The download button could not be found.")
                    return
                tag_link = requests.get(tag_link).url
                if '/tag/' not in tag_link:
                    print(
                        f"Error: Unable to find the latest version in {tag_link}.")
                    return
                download_link = tag_link.replace('tag', 'download')

                # CPU Architecture
                arch = platform.machine()
                print(f'Architecture: {arch}')

                # Searching for assets with Architecture
                assets_page = requests.get(tag_link)
                assets_soup = BeautifulSoup(assets_page.content, 'html.parser')
                assets = assets_soup.find_all(
                    'span', attrs={'class': 'px-1 text-bold'})
                first_asset = assets[0]
                for asset in assets:
                    if asset.text.endswith('.AppImage'):
                        first_asset = asset
                        if arch in asset.text:
                            download(download_link=download_link,
                                     asset=asset, app=app)
                            return
                download(download_link=download_link,
                         asset=first_asset, app=app)
                return
        print(f"App {appimage} not found")


@ app.command()
def remove(
    appimage: str,
    force: bool = typer.Option(
        ...,
        prompt="Are you sure to remove this appimage?",
        help="Force deletion without confirmation.",
    ),
):
    """
    Remove an appimage.

    If --force is not used, will ask for confirmation.
    """
    if force:
        appimages = os.listdir(download_directory)
        for app in appimages:
            if appimage in app.lower():
                typer.echo(f"Deleting appimage: {app}")
                os.remove(f"{download_directory}/{app}")
                return
        typer.echo(f"No application is matching name: {appimage}")

    else:
        typer.echo("Operation cancelled")


@ app.command()
def updaterepo():
    """
    Update an list of appimages.

    If --force is not used, will ask for confirmation.
    """
    if not os.path.exists(program_list_directory):
        os.makedirs(program_list_directory)
    appimage_tags = soup.find_all("tr")
    appimages = []
    for appimage in appimage_tags:
        appid = str(appimage.get('id'))
        appid = appid.replace("/", "")
        appimages.append(appid)
    with open(program_list_file, 'w') as f:
        f.write('\n'.join(appimages))


if __name__ == "__main__":
    app()
