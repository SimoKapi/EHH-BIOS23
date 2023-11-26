import modules.extract
import json
import re

import fitz  # PyMuPDF

template = {
    1: [
        ["name", [30, 30, 90, 43]],
        ["export_date", [544, 44, 586, 54]],
        ["period_day", [156, 76, 192, 88]],
        ["time_range", [30, 74, 158, 86]],
        ["tc_vh_%", [550, 144, 582, 155]],
        ["tc_h_%", [550, 188, 582, 200]],
        ["tc_n_%", [550, 228, 582, 239]],
        ["tc_l_%", [550, 262, 582, 274]],
        ["tc_vl_%", [550, 285, 582, 297]],

        ["sensor_usage_%", [291, 130, 319, 144]],

        ["glucose_average", [285, 261, 329, 273]],
        ["glucose_variablity", [284, 290, 334, 305]],

        ["gmi_%", [225, 278, 262, 288]],

        # ["insulin_basal", [625, 490, 648, 498]],
        # ["insulin_bolus", [625, 461, 649, 471]]
    ]
}

def libreview_type_1(pdf_path):

    output = {
        "type": "LibreView_1",
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

    period_day = re.search("(\d+,?\d*)", output["period_day"])
    time_range = re.findall("(\d{1,2}.\s?.*?\d{4})", output["time_range"])

    tc_vh = re.search("(\d+,?\d*)\s?%", output["tc_vh_%"])
    tc_h = re.search("(\d+,?\d*)\s?%", output["tc_h_%"])
    tc_n = re.search("(\d+,?\d*)\s?%", output["tc_n_%"])
    tc_l = re.search("(\d+,?\d*)\s?%", output["tc_l_%"])
    tc_vl = re.search("(\d+,?\d*)\s?%", output["tc_vl_%"])

    gmi = re.search("(\d+,?\d*)\s?%", output["gmi_%"])
    sensor_usage = re.search("(\d+,?\d*)\s?%", output["sensor_usage_%"])



    output["period_day"] = period_day and period_day.group(1)

    output["from"] = time_range and time_range[0]
    output["to"] = time_range and time_range[1]
    del output["time_range"]

    output["tc_vh_%"] = tc_vh and tc_vh.group(1)
    output["tc_h_%"] = tc_h and tc_h.group(1)
    output["tc_n_%"] = tc_n and tc_n.group(1)
    output["tc_l_%"] = tc_l and tc_l.group(1)
    output["tc_vl_%"] = tc_vl and tc_vl.group(1)

    output["gmi_%"] = gmi and gmi.group(1)
    output["sensor_usage_%"] = sensor_usage and sensor_usage.group(1)

    print(json.dumps(output, indent=4))
    return output
