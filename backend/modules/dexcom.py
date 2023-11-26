import modules.extract
import json
import re

import fitz  # PyMuPDF

template = {
    1: [
        ["name", [454, 56, 594, 67]],
        ["period_day", [19, 56, 58, 68]],
        ["time_range", [64, 56, 170, 67]],
        ["export_date", [531, 746, 592, 755]],
        ["tc_vh_%", [276, 129, 298, 141]],
        ["tc_h_%", [276, 147, 298, 159]],
        ["tc_n_%", [276, 165, 298, 179]],
        ["tc_l_%", [276, 183, 298, 197]],
        ["tc_vl_%", [276, 200, 298, 214]],

        ["sensor_usage_%", [464, 139, 502, 160]],

        ["glucose_average", [18, 124, 147, 176]],
        ["glucose_variablity", [20, 228, 105, 248]],

        ["gmi_%", [137, 225, 192, 252]],

        # ["type", [160, 55, 730, 300]] 
    ]
}

def dexcom_type_1(pdf_path):

    output = {
        "type": "Dexcom_1",
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
    export_date = re.search("(\d.*?\d\d\d\d)", output["export_date"])

    tc_vh = re.search("(\d+,?\d*)\s?%", output["tc_vh_%"])
    tc_h = re.search("(\d+,?\d*)\s?%", output["tc_h_%"])
    tc_n = re.search("(\d+,?\d*)\s?%", output["tc_n_%"])
    tc_l = re.search("(\d+,?\d*)\s?%", output["tc_l_%"])
    tc_vl = re.search("(\d+,?\d*)\s?%", output["tc_vl_%"])

    gmi = re.search("(\d+,?\d*)\s?%", output["gmi_%"])
    sensor_usage = re.search("(\d+,?\d*)\s?%", output["sensor_usage_%"])


    output["period_day"] = period_day and period_day.group(1)
    output["export_date"] = export_date and export_date.group(1)
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
