import modules.extract
import modules.glooko
import modules.dexcom
import modules.medtronic
import modules.libreview

import fitz  # PyMuPDF
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

import codecs

import os
import traceback

pdfsDir = "pdfs"
result = {}

def analyze_report(path):
    file_name = path

    pdf_document = fitz.open(file_name)
    if(modules.extract.extract_text_from_pdf(pdf_document, 1, (21, 119, 78, 135)).find("Glooko") != -1):
        # print("Glooko1")
        modules.glooko.glooko_type_1(file_name)
        return True
    if(modules.extract.extract_text_from_pdf(pdf_document, 1, (115, 768, 141, 778)).find("Glooko") != -1):
        # print("Glooko2")
        modules.glooko.glooko_type_2(file_name)
        return True
    if(modules.extract.extract_text_from_pdf(pdf_document, 1, (20, 747, 39, 754)).find("Dexcom") != -1):
        # print("Dexcom1")
        modules.dexcom.dexcom_type_1(file_name)
        return True
    if(modules.extract.extract_text_from_pdf(pdf_document, 1, (29, 56, 120, 75)).find("AGP report") != -1):
        # print("LibreView1")
        modules.libreview.libreview_type_1(file_name)
        return True
    fp = open(file_name, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    if("Author" in doc.info[0] and "Medtronic" in codecs.decode(doc.info[0]["Author"], "utf-8", "ignore").replace('\x00', "")):
        # print("Medtronic1")
        modules.medtronic.medtronic_type_1(file_name)
        return True
    return False

for file in os.listdir(pdfsDir):
    tempRes = analyze_report(os.path.join(pdfsDir, file))
# analyze_report("pdfs/test2.pdf")
# analyze_report("pdfs/test4.pdf")
# analyze_report("pdfs/test5.pdf")
# analyze_report("f4116865-5d15-4e1b-9b36-c33a5df5eefe.pdf")
# directory = '/home/nullxwp87/Documents/PDFS/new/gly1/gly1/'
# fp = open("/home/nullxwp87/Documents/PDFS/new/gly1/logs/filetrack.log", 'w')
 
# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     # checking if it is a file
#     if os.path.isfile(f):
#         try:
#             if(analyze_report(f)):
#                 print("Done. ", filename)
#             else:
#                 print("Unknown Template ", filename)
#         except Exception as e:
#             print(f, traceback.format_exc())
#             # if current_text is not None:
#             fp.write(f + "\n")
#             fp.flush()
#             # fp.close()
#         # print("Done.")