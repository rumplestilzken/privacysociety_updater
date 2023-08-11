import platform
import sys
import os
import urllib.request
import zipfile
import json
import stat
import tarfile

import lzma

from enum import Enum


class OS(Enum):
    NotSet = ""
    Linux = "linux"
    Windows = "windows"


class DeviceType(Enum):
    NotSet = ""
    Pocket = "pocket"
    Jelly2E = "jelly2e"
    AtomL = "atoml"
    Pixel5a = "pixel5a"


os_type = OS.NotSet
progress_bar = None
filename = ""
outfile = ""
dev = DeviceType.NotSet


def get_variant_map():
    dict = {"Titan Pocket": "lineage_privacysociety_pocket",
            "Jelly 2E": "lineage_privacysociety_jelly2e",
            "Atom L": "lineage_privacysociety_atoml",
            "Pixel 5a": "lineage_privacysociety_pixel5a", }
    return dict


def download_update(json_url, variant):
    global dev
    here = os.path.dirname(os.path.realpath(__file__))
    json_contents = urllib.request.urlopen(json_url)
    data = json.load(json_contents)
    variants = data["variants"]
    # print(variant)
    variant_code = get_variant_map()[variant]
    for enm in DeviceType:
        if variant_code.split("_")[2] in enm.value:
            dev = enm
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

    if not os.path.exists(outfile.strip(".xz")) and ".xz" in outfile:
        print("Extracting PrivacySociety GSI '" + outfile + "'")
        with lzma.open(outfile) as f, open(outfile.strip(".xz"), 'wb') as fout:
            file_content = f.read()
            fout.write(file_content)

    if not os.path.exists(outfile.strip(".tar.gz") and ".tar.gz" in outfile):
        print("Extracting PrivacySociety GSI '" + outfile + "'")
        with tarfile.open(outfile, "r") as tf:
            tf.extractall(path=here + "/resources/")


def process_flash(json_url, variant, progressbar):
    global progress_bar
    progress_bar = progressbar
    progressbar.setValue(10)

    prepare_adb_and_fastboot()
    progressbar.setValue(20)

    download_update(json_url, variant)
    progressbar.setValue(50)

    if not dev == DeviceType.Pixel5a:
        flash_gsi()
    else:
        flash_lineage_package()


def prepare_adb_and_fastboot():
    here = os.path.dirname(os.path.realpath(__file__))

    global filename
    global os_type
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

    exe = full_path.rstrip(".zip") + "/platform-tools/adb"
    st = os.stat(exe)
    os.chmod(exe, st.st_mode | stat.S_IEXEC)
    exe = full_path.rstrip(".zip") + "/platform-tools/fastboot"
    st = os.stat(exe)
    os.chmod(exe, st.st_mode | stat.S_IEXEC)


def flash_lineage_package():
    return


def flash_gsi():
    here = os.path.dirname(os.path.realpath(__file__))
    global filename
    global os_type
    global outfile

    full_path = here + "/resources/" + filename.rstrip(".zip") + "/platform-tools/"
    command = "/adb reboot bootloader"

    os.system(full_path + command)

    progress_bar.setValue(70)
    command = "/fastboot flash super " + outfile.rstrip(".xz").rstrip(".tar.gz")
    os.system(full_path + command)

    command = "/fastboot reboot"
    os.system(full_path + command)

    progress_bar.setValue(90)
