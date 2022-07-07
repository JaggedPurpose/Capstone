#! /usr/bin/env python3

import re
import email
import mimetypes
import os
from docx2pdf import convert
import hashlib
from fpdf import FPDF

name_pattern = r"([a-zA-Z]+)\s?([a-zA-Z]+\s)([a-zA-Z]+)"
email_pattern = r"(\d+)?(\w+)@(\w+)\.(\w+)"


def main():
    doc = input("Example: C:\\Users\junwo\PycharmProjects\\NSAA\Capstone\\test.docx"
                "\nPlease provide the absolute path to the .docx file to be converted into a PDF as the above example: ")
    convert_doc(doc)
    # print(md5sum(doc))
    # print(name_checksum(requester))
    # total_checksum(md5sum(doc), name_checksum())
    doc_sum = md5sum(doc)
    total_sum = total_checksum(doc_sum, name_checksum())
    watermarker_pdf(pdf_md5=doc_sum, total_md5=total_sum, doc_path=doc)


def convert_doc(doc_file):
    # Separate the path/file and extension
    pdf_name = os.path.splitext(doc_file)[0] + ".pdf"
    # Check if the file exists
    if os.path.exists(doc_file):
        # convert the doc_file to pdf with the pdf extension
        convert(doc_file, pdf_name)
        print(f"Docx file has been converted to PDF. This can be found at {pdf_name}")
    elif not os.path.exists(doc_file):
        print("Please check if you have provided a valid file with the path")
        main()


def md5sum(pdf_file):
    # call out the correct file, which in this case would be the converted pdf
    pdf_file = os.path.splitext(pdf_file)[0] + ".pdf"
    # open the pdf file
    with open(pdf_file, 'rb') as pdf:
        # read the pdf file
        file_pdf = pdf.read()
        checksum = hashlib.md5(file_pdf).hexdigest()
        return checksum


def name_checksum():
    requester = input("What is the full name of the of the document requester? You may include the middle name. ")
    # make sure the name format matches the requested input
    result = re.match(name_pattern, requester)
    if not result:
        print("Please provide the name in a valid format."
              "\nExamples: Junwon Suh, John Christopher Depp, ")
        name_checksum()
    # elif result: # if the function looks back even with the correct format, comment out the below and un-comment this
    else:
        # using hashlib.md5() take in the arg of the function and make sure to encode
        name_sum = hashlib.md5(requester.encode())
        # return the md5sum of the requester
        return name_sum.hexdigest()


# for total_checksum(), 2 args will be the return values of the md5sum() and name_checksum()
def total_checksum(pdf_md5, name_md5):
    # turn the return values from the arguments into a string
    pdf_sum = f"{pdf_md5}"
    print(f"MD5 checksum of the PDF: {pdf_sum}") # this can be un-commented to check the md5sum of the pdf file
    name_sum = f"{name_md5}"
    print(f'MD5 checksum of the requester: {name_sum}') # this can be un-commented to check the md5sum of the requester's name
    # set a new variable that will take the str of above checksums
    total_sum = f"{pdf_sum}{name_sum}"
    checksum = hashlib.md5(total_sum.encode())
    print(f"Combined MD5 checksum of the PDF and the requester: {checksum.hexdigest()}")
    return checksum.hexdigest()


def watermarker_pdf(doc_path, pdf_md5, total_md5):
    watermarker_name = os.path.splitext(doc_path)[0] + "_watermarker.pdf"
    pdf_sum = f"{pdf_md5}"
    total_sum = f"{total_md5}"
    watermarker = FPDF()
    watermarker.add_page()
    watermarker.set_font("Times", size=10)
    watermarker.cell(200, 5, txt=f"{pdf_sum}", ln=1, align='C')
    watermarker.cell(200, 5, txt=f"{total_sum}", ln=2, align='C')
    watermarker.set_text_color(255, 255, 255)
    watermarker.cell(200, 200, txt=f"{total_sum} ", ln=1, align='C')
    watermarker.output(watermarker_name)
    print(f"The watermark PDF can be found at: {watermarker_name}")


if __name__ == "__main__":
    main()
