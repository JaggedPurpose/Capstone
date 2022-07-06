#! /usr/bin/env python3

import re
import email
import mimetypes
import os
from docx2pdf import convert
import hashlib


def main():
    doc = input("Example: C:\<user>\Desktop\\file.docx"
                "\nPlease provide the .docx file to be converted into a PDF as the above example: ")
    requester = input("What is the full name of the document requester? ")
    convert_doc(doc)
    md5sum(doc)
    name_checksum(requester)


def convert_doc(doc_file):
    # Separate the path/file and extension
    pdf_name = os.path.splitext(doc_file)[0] + ".pdf"
    # convert the doc_file to pdf with the pdf extension
    convert(doc_file, pdf_name)
    print("Docx file has been converted to PDF")


def md5sum(pdf_file):
    # call out the correct file, which in this case would be the converted pdf
    pdf_file = os.path.splitext(pdf_file)[0] + ".pdf"
    # open the pdf file
    with open(pdf_file, 'rb') as pdf:
        # read the pdf file
        file_pdf = pdf.read()
        checksum = hashlib.md5(file_pdf).hexdigest()
        return checksum


def name_checksum(name):
    # using hashlib.md5() take in the arg of the function and make sure to encode
    name_sum = hashlib.md5(name.encode())
    # return the md5sum of the requester
    return name_sum.hexdigest()


# for total_checksum(), 2 args will be the return values of the md5sum() and name_checksum()
def total_checksum(pdf_md5, name_md5):
    # turn the return values from the arguments into a string
    pdf_sum = f"{pdf_md5}"
    # print(pdf_sum) # this can be un-commented to check the md5sum of the pdf file
    name_sum = f"{name_md5}"
    # print(name_sum) # this can be un-commented to check the md5sum of the requester's name
    # set a new variable that will take the str of above checksums
    total_sum = f"{pdf_sum}{name_sum}"
    checksum = hashlib.md5(total_sum.encode())
    return checksum.hexdigest()


if __name__ == "__main__":
    main()
