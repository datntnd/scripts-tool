import os 
from pathlib import Path
import cv2 
from glob import glob
from matplotlib import pyplot as plt
import json 


def get_label_plate(path_folder):
    # exmaple path_folder = 'output/baria/001/2022-12-14/lp/1670995353_32264'
    # folder palte: 'plate/baria/001/2022-12-14/1670995353_32264.jpg'
    list_split_path = path_folder.split("/")

    # replace output to plate 
    plate_folder = "plate/" + "/".join(list_split_path[1:4]) 
    Path(plate_folder).mkdir(parents=True, exist_ok=True)
    # print(f"plate_folder: {plate_folder}")


    plate_ocr_folder = "plate_ocr/" + "/".join(list_split_path[1:4])
    Path(plate_ocr_folder).mkdir(parents=True, exist_ok=True)
    # print(f"plate_ocr_folder: {plate_ocr_folder}")


    file_name = list_split_path[-1] # 1670995353_32264


    # plate label
    image = cv2.imread(f"{path_folder}/c.jpg")
    template = cv2.imread(f"{path_folder}/cc.jpg")

    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)

    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    # print(minVal, maxVal, minLoc, maxLoc)
    (x, y) = maxLoc
    w, h, _ = template.shape
    w_image = image.shape[0]
    h_image = image.shape[1]
    x_center = x + w /2 
    y_center = y + h /2 
    
    file_plate_image_name = f"{plate_folder}/{file_name}.jpg"
    
    cv2.imwrite(file_plate_image_name, image)


    with open(f"{plate_folder}/{file_name}.txt", "w") as f:
        # c, x_min, y_min, w, h
        f.write(f"0 {x_center} {y_center} {w} {h}\n")
        f.write(f"0 {x_center/w_image} {y_center/h_image} {w/w_image} {h/h_image}\n")


    # plate ocr label
    file_ocr_image_name = f"{plate_ocr_folder}/{file_name}.jpg"

    cv2.imwrite(file_ocr_image_name, template)
    data = json.load(open(f"{path_folder}/info.json"))
    with open(f"{plate_ocr_folder}/label.txt", "a") as f:
        # c, x_min, y_min, w, h
        f.write(f"{file_ocr_image_name}\t{data['lp']}\n")


list_folder = glob("output/*/*/*/lp/*", recursive = True)
for path_folder in list_folder:
    list_file = glob(f"{path_folder}/*")
    if len(list_file) == 4:
        get_label_plate(path_folder)
    else:
        print(path_folder)
