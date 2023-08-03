import sys
import os
import urllib.request
import zipfile
import json

from PyQt5.QtWidgets import QComboBox

from enum import Enum

class OS(Enum):
    NotSet = ""
    Linux = "linux"
    Windows = "windows"

os_type = OS.NotSet
progress_bar = None

def get_variant_map():
    dict = {"Titan Pocket": "lineage_privacysociety_pocket",
            "Jelly 2E": "lineage_privacysociety_jelly2e",
            "Atom L": "lineage_privacysociety_atoml" }
    return dict

def download_update(json_url, variant):
    here = os.path.dirname(os.path.realpath(__file__))
    json_contents = urllib.request.urlopen(json_url)
    data = json.load(json_contents)
    variants = data["variants"]
    # print(variant)
    variant_code = get_variant_map()[variant]
    # print(variant_code)
    variant_url = "";
    for i in variants:
        if variant_code == i["name"]:
            variant_url = i["url"];
    # print(variant_url)

    outfile = here + "/resources/" + os.path.basename(variant_url)
    if not os.path.exists(outfile):
        urllib.request.urlretrieve(variant_url, outfile)
def process_flash(json_url, variant, progressbar):
    progress_bar = progressbar
    # ui.applyProgress(10)

    prepare_adb_and_fastboot()
    download_update(json_url, variant)

    download_new_gsi()


def prepare_adb_and_fastboot():
    here = os.path.dirname(os.path.realpath(__file__))
    # ui.applyProgress(10)
    filename = ""
    if 'linux' in sys.platform:
        os_type = OS.Linux
        filename = "platform-tools_r34.0.4-linux.zip"
    elif 'win' in sys.platform:
        os_type = OS.Windows
        filename = "platform-tools_r34.0.4-windows.zip"

    url = "https://github.com/rumplestilzken/privacysociety_updater/releases/download/resources/" + filename

    full_path = here + "/resources/" + filename

    # Download
    if not os.path.exists(full_path):
        urllib.request.urlretrieve(url, full_path)

    # Unzip
    if not os.path.exists(full_path.strip(".zip")):
        with zipfile.ZipFile(full_path, 'r') as zip_ref:
            zip_ref.extractall(full_path.strip(".zip"))


def download_new_gsi():

   # progress_bar.setValue(10)
    return

def put_phone_in_fastboot_mode():
    return


def flash_gsi():
    return
