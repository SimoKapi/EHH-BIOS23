import modules.extract
import json
import re
import math
import fitz  # PyMuPDF

# from PIL import Image
# from PIL import ImageShow
import cv2
import numpy as np
import io
from sklearn.cluster import KMeans

colrs = {
    0: [196, 42, 43],
    1: [246, 164, 166],
    2: [137, 208, 135],
    3: [251, 225, 152],#[208, 222, 163], [251, 225, 152]
    4: [247, 206, 88]
}

template = {
    1: [
        ["name", [245, 16, 572, 55]],
        ["export_date", [625, 33, 701, 41]],
        ["period_day", [213, 44, 244, 53]],
        ["time_range", [135, 44, 213, 53]],
        ["tc_vh_%", [276, 129, 298, 141]],
        ["tc_h_%", [276, 147, 298, 159]],
        ["tc_n_%", [276, 165, 298, 179]],
        ["tc_l_%", [276, 183, 298, 197]],
        ["tc_vl_%", [276, 200, 298, 214]],
        # ["tc_rect", [40, 321, 61, 503]],
        ["sensor_usage_%", [621, 354, 639, 363]],

        ["glucose_average", [611, 368, 624, 377]],
        ["glucose_variablity", [630, 368, 643, 377]],

        ["gmi_%", [602, 381, 623, 391]],

        ["insulin_basal", [625, 490, 648, 498]],
        ["insulin_bolus", [625, 461, 649, 471]]

        # ["type", [160, 55, 730, 300]] 
    ]
}

def medtronic_type_1(pdf_path):

    output = {
        "type": "Medtronic_1",
        "path": pdf_path
    }
    
    pdf_document = fitz.open(pdf_path)
    for i in template.keys():
        for j in template[i]:
            x,y,w,z = j[1][0], j[1][1], j[1][2], j[1][3]  
            
            page_number = i # Change this to the desired page number
            rectangular_area = (x, y, w, z)  # Change this to the coordinates of your desired area

            text = modules.extract.extract_text_from_pdf(pdf_document, page_number, rectangular_area)

            # print(text)
            output[j[0]] = text

    pixmap = pdf_document[0].get_pixmap(clip=(37, 319, 184, 507))
    # img = Image.open(io.BytesIO(pixmap.tobytes()))

    nparr = np.fromstring(pixmap.tobytes(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    crop_img = img[2:182, 24:62]
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    rows,cols,_ = crop_img.shape

    colours = []
    filteredColors = []
    resultArray = set()

    for i in range(rows):
        row_index = i
        row = crop_img[row_index, :]

        average_color = np.mean(row, axis=0)
        average_color = average_color.astype(int)
        average_color = average_color[::-1]
        colours.append(list(average_color))
        if list(average_color) not in filteredColors:
            filteredColors.append(list(average_color))
            resultArray.add(getClosestColor(list(average_color)))
    resultArray = list(resultArray)
    resultArray.sort()
    print(resultArray)

    # Calculate distance between colors
    # threshold = 50
    # uniqueColorsCount = 0
    # uniqueColors = []
    # for i in range(len(filteredColors) - 1):
    #     distance = dist(filteredColors[i], filteredColors[i+1])
    #     if distance > threshold:
    #         uniqueColorsCount+=1
    #         smallest = 5
    #         smallestDist = 100000
    #         for j in colrs.keys():
    #             if dist(colrs[j], filteredColors[i+1]) < smallestDist:
    #                 smallest = j
    #                 smallestDist = dist(colrs[j], filteredColors[i+1])
    #         uniqueColors.append(smallest)
    # uniqueColors.sort()
    # print(uniqueColors)

    # print(img.size[0])
    # print(img.size[1])
    # ImageShow.show(img)
    # color = img.getpixel((43,181))
    # print(color)

    # def get_colour(color):
    #     if(
    #         (color[0] > 240 - 10 and color[0] < 240 + 10)
    #         and (color[1] > 170 - 20 and color[1] < 170 + 20)
    #         and (color[0] > 240 - 10 and color[0] < 240 + 10)
    #     ):
    #         print("light_red")
    #     elif(
    #         (color[0] > 138 - 10 and color[0] < 138 + 10)
    #         and (color[1] > 209 - 10 and color[1] < 209 + 10)
    #         and (color[0] > 139 - 10 and color[0] < 139 + 10)
    #     ):
    #         print("green")
    #     elif(
    #         (color[0] > 250 - 5 and color[0] < 250 + 5)
    #         and (color[1] > 240 - 5 and color[1] < 240 + 5)
    #         and (color[0] > 180 - 15 and color[0] < 180 + 15)
    #     ):
    #         print("light_yellow")
    

    # get_colour(img.getpixel((43,181)))
    # get_colour(img.getpixel((43,182)))
    # get_colour(img.getpixel((40,181)))
    # get_colour(img.getpixel((50,181)))
    # print()
    # print()
    # get_colour(img.getpixel((43,150)))
    # get_colour(img.getpixel((43,140)))
    # get_colour(img.getpixel((40,160)))
    # get_colour(img.getpixel((50,170)))
    # print()
    # print()
    # get_colour(img.getpixel((43,12)))
    # get_colour(img.getpixel((43,30)))
    # get_colour(img.getpixel((40,18)))
    # get_colour(img.getpixel((50,20)))


    name = re.search("(.*),\s?(.*)", output["name"])
    period_day = re.search("\((\d+)", output["period_day"])
    export_date = re.search("(\d.*?\d\d\d\d)", output["export_date"])
    time_range = re.findall("(\d{1,2}.\s?.*?\d{4})", output["time_range"])

    # tc_vh = re.search("(\d+,?\d*)\s?%", output["tc_vh_%"])
    # tc_h = re.search("(\d+,?\d*)\s?%", output["tc_h_%"])
    # tc_n = re.search("(\d+,?\d*)\s?%", output["tc_n_%"])
    # tc_l = re.search("(\d+,?\d*)\s?%", output["tc_l_%"])
    # tc_vl = re.search("(\d+,?\d*)\s?%", output["tc_vl_%"])

    gmi = re.search("(\d+,?\d*)\s?%", output["gmi_%"])
    sensor_usage = re.search("(\d+,?\d*)\s?%", output["sensor_usage_%"])

    output["name"] = name and name.group(2) + " " + name.group(1)
    output["export_date"] = export_date and export_date.group(1)
    output["period_day"] = period_day and period_day.group(1)

    output["from"] = time_range and time_range[0]
    output["to"] = time_range and time_range[1]
    del output["time_range"]

    # output["tc_vh_%"] = tc_vh and tc_vh.group(1)
    # output["tc_h_%"] = tc_h and tc_h.group(1)
    # output["tc_n_%"] = tc_n and tc_n.group(1)
    # output["tc_l_%"] = tc_l and tc_l.group(1)
    # output["tc_vl_%"] = tc_vl and tc_vl.group(1)

    output["gmi_%"] = gmi and gmi.group(1)
    output["sensor_usage_%"] = sensor_usage and sensor_usage.group(1)

    print(json.dumps(output, indent=4))
    return output

def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def getClosestColor(a):
    smallest = 5
    smallestDist = 100000
    for j in colrs.keys():
        if dist(colrs[j], a) < smallestDist:
            smallest = j
            smallestDist = dist(colrs[j], a)
    return smallest