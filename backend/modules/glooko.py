import modules.extract
import json
import re

import fitz  # PyMuPDF

template_1 = {
    1: [
        ["name", [280, 60, 594, 92]],
        ["sensor_usage_%", [67, 201, 93, 212]],
    ],
    2: [
        ["time_range", [407, 22, 545, 35]],
        ["period_day", [545, 24, 585, 37]],
        ["export_date", [498, 37, 584, 50]],

        ["tc_vh_%", [107, 125, 124, 129]],
        ["tc_h_%", [106, 131, 124, 139]],
        ["tc_n_%", [107, 142, 124, 150]],
        ["tc_l_%", [107, 155, 124, 163]],
        ["tc_vl_%", [107, 164, 124, 172]],

        ["glucose_average", [107, 185, 145, 195]],
        ["glucose_variablity", [107, 195, 146, 204]],
    ]
}

def glooko_type_1(pdf_path):

    output = {
        "type": "Glooko_1",
        "path": pdf_path
    }
    
    pdf_document = fitz.open(pdf_path)
    for i in template_1.keys():
        for j in template_1[i]:
            x,y,w,z = j[1][0], j[1][1], j[1][2], j[1][3]  
            
            page_number = i # Change this to the desired page number
            rectangular_area = (x, y, w, z)  # Change this to the coordinates of your desired area

            text = modules.extract.extract_text_from_pdf(pdf_document, page_number, rectangular_area)

            output[j[0]] = text

    name = re.search("(.*)\n", output["name"])
    sensor_usage = re.search("(\d+,?\d*)%", output["sensor_usage_%"])
    time_range = re.search("(\d.*?\d\d\d\d)[.\n\s-]*?(\d.*\d\d\d\d)\n", output["time_range"])
    period_day = re.search("\((\d+)", output["period_day"])
    export_date = re.search("Dnes:\s?(.*)", output["export_date"])

    tc_vh = re.search("(\d+,?\d*)\s?%", output["tc_vh_%"])
    tc_h = re.search("(\d+,?\d*)\s?%", output["tc_h_%"])
    tc_n = re.search("(\d+,?\d*)\s?%", output["tc_n_%"])
    tc_l = re.search("(\d+,?\d*)\s?%", output["tc_l_%"])
    tc_vl = re.search("(\d+,?\d*)\s?%", output["tc_vl_%"])

    output["name"] = name and name.group(1)
    output["sensor_usage_%"] = sensor_usage and sensor_usage.group(1)
    
    output["from"] = time_range and time_range.group(1)
    output["to"] = time_range and time_range.group(2)
    del output["time_range"]

    output["period_day"] = period_day and period_day.group(1)
    output["export_date"] = export_date and export_date.group(1)

    output["tc_vh_%"] = tc_vh and tc_vh.group(1)
    output["tc_h_%"] = tc_h and tc_h.group(1)
    output["tc_n_%"] = tc_n and tc_n.group(1)
    output["tc_l_%"] = tc_l and tc_l.group(1)
    output["tc_vl_%"] = tc_vl and tc_vl.group(1)

    print(json.dumps(output, indent=4))
    return output
















template_2 = {
    1: [
        ["name", [20, 1, 323, 21]],
        ["time_range", [395, 23, 547, 37]],
        ["period_day", [545, 24, 585, 37]],
        ["export_date", [498, 37, 584, 50]],
        ["insulin_basal", [464, 111, 480, 120]],
        ["insulin_bolus", [464, 131, 480, 140]]
    ],
    2: [
        ["sensor_usage_%", [281, 153, 320, 167]],

        ["tc_vh_%", [58, 93, 77, 102]],
        ["tc_h_%", [58, 109, 77, 117]],
        ["tc_n_%", [58, 125, 77, 133]],
        ["tc_l_%", [58, 141, 77, 149]],
        ["tc_vl_%", [58, 157, 77, 165]],

        ["glucose_average", [285, 128, 342, 140]],
        ["glucose_variablity", [493, 87, 534, 100]],
        
        ["gmi_%", [277, 100, 306, 113]],

    ]
}





def glooko_type_2(pdf_path):

    output = {
        "type": "Glooko_2",
        "path": pdf_path
    }

    pdf_document = fitz.open(pdf_path)
    for i in template_2.keys():
        for j in template_2[i]:
            x,y,w,z = j[1][0], j[1][1], j[1][2], j[1][3]  
            
            page_number = i # Change this to the desired page number
            rectangular_area = (x, y, w, z)  # Change this to the coordinates of your desired area

            text = modules.extract.extract_text_from_pdf(pdf_document, page_number, rectangular_area)

            output[j[0]] = text

    sensor_usage = re.search("(\d+,?\d*)%", output["sensor_usage_%"])
    period_day = re.search("\((\d+)", output["period_day"])
    export_date = re.search("Dnes:\s?(.*)", output["export_date"])
    time_range = re.search("(\d.*?\d\d\d\d)[.\n\s-]*?(\d.*\d\d\d\d)\n", output["time_range"])

    tc_vh = re.search("(\d+,?\d*)\s?%", output["tc_vh_%"])
    tc_h = re.search("(\d+,?\d*)\s?%", output["tc_h_%"])
    tc_n = re.search("(\d+,?\d*)\s?%", output["tc_n_%"])
    tc_l = re.search("(\d+,?\d*)\s?%", output["tc_l_%"])
    tc_vl = re.search("(\d+,?\d*)\s?%", output["tc_vl_%"])

    gmi = re.search("(\d+,?\d*)\s?%", output["gmi_%"])


    output["tc_vh_%"] = tc_vh and tc_vh.group(1)
    output["tc_h_%"] = tc_h and tc_h.group(1)
    output["tc_n_%"] = tc_n and tc_n.group(1)
    output["tc_l_%"] = tc_l and tc_l.group(1)
    output["tc_vl_%"] = tc_vl and tc_vl.group(1)

    output["gmi_%"] = gmi and gmi.group(1)

    output["from"] = time_range and time_range.group(1)
    output["to"] = time_range and time_range.group(2)
    del output["time_range"]

    output["sensor_usage_%"] = sensor_usage and sensor_usage.group(1)
    output["period_day"] = period_day and period_day.group(1)
    output["export_date"] = export_date and export_date.group(1)

    print(json.dumps(output, indent=4))
    return output
