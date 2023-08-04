import sys
import os
import urllib.request
import zipfile
import json
import stat

import lzma

from enum import Enum

import ui


class OS(Enum):
    NotSet = ""
    Linux = "linux"
    Windows = "windows"


os_type = OS.NotSet
progress_bar = None
filename = ""
outfile = ""


def get_variant_map():
    dict = {"Titan Pocket": "lineage_privacysociety_pocket",
            "Jelly 2E": "lineage_privacysociety_jelly2e",
            "Atom L": "lineage_privacysociety_atoml"}
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

    global outfile
    outfile = here + "/resources/" + os.path.basename(variant_url)
    if not os.path.exists(outfile):
        urllib.request.urlretrieve(variant_url, outfile)

    global progress_bar
    progress_bar.setValue(30)

    if not os.path.exists(outfile.strip(".xz")):
        with lzma.open(outfile) as f, open(outfile.strip(".xz"), 'wb') as fout:
            file_content = f.read()
            fout.write(file_content)


def process_flash(json_url, variant, progressbar):
    global progress_bar
    progress_bar = progressbar
    progressbar.setValue(10)
    # ui.applyProgress(10)

    prepare_adb_and_fastboot()
    progressbar.setValue(20)
    download_update(json_url, variant)
    progressbar.setValue(40)
    flash_gsi()
    progressbar.setValue(50)


def prepare_adb_and_fastboot():
    here = os.path.dirname(os.path.realpath(__file__))
    # ui.applyProgress(10)
    global filename
    filename = ""
    if 'linux' in sys.platform:
        os_type = OS.Linux
        filename = "platform-tools_r34.0.4-linux.zip"
    elif 'win' in sys.platform:
        os_type = OS.Windows
        filename = "platform-tools_r34.0.4-windows.zip"

    url = "https://github.com/rumplestilzken/privacysociety_updater/releases/download/resources/" + filename

    full_path = here + "/resources/" + filename

    exe = full_path.rstrip(".zip") + "/platform-tools/adb"
    st = os.stat(exe)
    os.chmod(exe, st.st_mode | stat.S_IEXEC)
    exe = full_path.rstrip(".zip") + "/platform-tools/fastboot"
    st = os.stat(exe)
    os.chmod(exe, st.st_mode | stat.S_IEXEC)

    # Download
    if not os.path.exists(full_path):
        urllib.request.urlretrieve(url, full_path)

    # Unzip
    if not os.path.exists(full_path.strip(".zip")):
        with zipfile.ZipFile(full_path, 'r') as zip_ref:
            zip_ref.extractall(full_path.strip(".zip"))


def flash_gsi():
    here = os.path.dirname(os.path.realpath(__file__))
    global filename
    global os_type
    global outfile

    full_path = here + "/resources/" + filename.rstrip(".zip") + "/platform-tools/"
    command = "/adb reboot bootloader"

    os.system(full_path + command)

    progress_bar.setValue(70)
    command = "/fastboot flash super " + outfile.rstrip(".xz")
    os.system(full_path + command)

    command = "/fastboot reboot"
    os.system(full_path + command)

    progress_bar.setValue(90)
