from datetime import datetime
import shutil
from time import sleep
from os import listdir
from os.path import isfile, join
import glob
from pathlib import Path


local = "baria"
list_cam = [f"{number:03d}" for number in range(1,3)]
SCR_DIR = "/home/vtcc/uTVM/output"
TARG_DIR = "/u02/vts/utvm/output"


# while True:
folder = datetime.now().strftime("%Y-%m-%d")
for cam in list_cam:
    src_path = f"{SCR_DIR}/{local}/{cam}/{folder}/lp"
    targ_path = f"{TARG_DIR}/{local}/{cam}/{folder}/lp"

    Path(targ_path).mkdir(parents=True, exist_ok=True)
    list_src_folders = listdir(src_path)
    list_targ_folders = listdir(targ_path)

    print(list_src_folders)
    print(list_targ_folders)

    for i in list_src_folders:
        src_dir = f"{src_path}/{i}"
        number_file = len(glob.glob(f"{src_path}/{i}/*"))
        if number_file == 4 and i not in list_targ_folders:
            dest_dir = f"{targ_path}/{i}"
            shutil.copytree(src_dir, dest_dir)


    list_src_folders = listdir(src_path)
    list_targ_folders = listdir(targ_path)

    print(f"{src_path}:{list_src_folders}")
    print(f"{targ_path}:{list_targ_folders}")