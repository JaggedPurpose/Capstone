#! /usr/bin/env python3

import re
import email
import mimetypes
import os
from docx2pdf import convert
import comtypes.client


def main():
    doc = input("Example: /home/<user>/Desktop/file.docx"
                "\nPlease provide the .docx file to be converted into a PDF as the above example: ")
    convert_doc(doc)


def convert_doc(doc_file):
    # wdFormatPDF = 17
    # word_doc = comtypes.client.CreateObject("Word.Application")
    # doc_file = word_doc.Documents.Open(doc_file)
    # doc_file.SaveAs(pdf_name, FileFormat=wdFormatPDF)
    # doc_file.Close()
    # word_doc.Quit()
    # convert(doc_file)
    pdf_name = os.path.splitext(doc_file)[0] + ".pdf"
    convert(doc_file, pdf_name)
    print("Docx file has been converted to PDF")


if __name__ == "__main__":
    main()
