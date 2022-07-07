#! /usr/bin/env python3
import sys
import re
import email
import mimetypes
import smtplib
import os
from docx2pdf import convert
import hashlib
from fpdf import FPDF
from PyPDF2 import PdfFileReader, PdfFileWriter

name_pattern = r"([a-zA-Z]+)\s?([a-zA-Z]+\s)([a-zA-Z]+)"
email_pattern = r"(\d+)?(\w+)@(\w+)\.(\w+)"


def main():
    print("This script is strictly for converting \".docx\" into a pdf with watermarking.")
    doc = input("Example: C:\\Users\junwo\PycharmProjects\\NSAA\Capstone\\test.docx"
                "\nPlease provide the absolute path to the .docx file to be converted into a PDF as the above example: ")
    convert_doc(doc)
    print(f"Docx file has been converted to PDF. This can be found at {os.path.splitext(doc)[0]}.pdf")
    doc_sum = md5sum(doc)
    requester = input("What is the full name of the of the document requester? You may include the middle name. ")
    total_sum = total_checksum(doc_sum, name_checksum(requester))
    watermarker_pdf(pdf_md5=doc_sum, total_md5=total_sum, doc_path=doc)
    pdfMerger(doc_file=doc)
    msg = generate(requester=requester, attachment_path=doc)
    send_email(msg, requester)
    sys.exit(1)


def convert_doc(doc_file):
    # Separate the path/file and extension
    pdf_name = os.path.splitext(doc_file)[0] + ".pdf"
    # Check if the file exists
    while True:
        try:
            if os.path.exists(doc_file):
                # convert the doc_file to pdf with the pdf extension
                convert(doc_file, pdf_name)
                return f"Docx file has been converted to PDF. This can be found at {pdf_name}"
            elif not os.path.exists(doc_file):
                print(f"{doc_file} does not exist.")
                print("Please check if you have provided a valid file with the path")
                main()
        except FileNotFoundError:
            print("Please try again after getting the correct file and its path")
            sys.exit(1)


def md5sum(pdf_file):
    # call out the correct file, which in this case would be the converted pdf
    pdf_file = os.path.splitext(pdf_file)[0] + ".pdf"
    # open the pdf file
    with open(pdf_file, 'rb') as pdf:
        # read the pdf file
        file_pdf = pdf.read()
        checksum = hashlib.md5(file_pdf).hexdigest()
        return checksum


def name_checksum(requester):
    # make sure the name format matches the requested input
    result = re.match(name_pattern, requester)
    if not result:
        rename = input("Examples: Junwon Suh, John Christopher Depp\nPlease provide the name in a valid format: ")
        return name_checksum(rename)
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
    watermarker.cell(200, 40, txt=f"{pdf_sum}", ln=1, align='C')
    watermarker.cell(200, -30, txt=f"{total_sum}", ln=2, align='C')
    watermarker.set_text_color(255, 255, 255)
    watermarker.cell(200, 200, txt=f"{total_sum} ", ln=1, align='C')
    watermarker.output(watermarker_name)
    print(f"The watermark PDF can be found at: {watermarker_name}")


def pdfMerger(doc_file):
    # Open and read the converted PDF and the watermarker
    pdf_file = PdfFileReader(open(f"{os.path.splitext(doc_file)[0]}.pdf", "rb"))
    watermarker = PdfFileReader(open(f"{os.path.splitext(doc_file)[0]}_watermarker.pdf", "rb"))
    # name of the watermarked PDf
    marked_pdf = os.path.splitext(doc_file)[0] + "_watermarked.pdf"
    # create a PDF writer
    watermarked = PdfFileWriter()
    # loop through the pages of the pdf_file and grab pages
    for pages in range(pdf_file.getNumPages()):
        # grab each page from above
        page = pdf_file.getPage(pages)
        # merge each page with the watermarker
        page.mergePage(watermarker.getPage(0))
        # add the merged page to the writer
        watermarked.addPage(page)
        with open(f"{os.path.splitext(doc_file)[0]}_watermarked.pdf", 'wb') as Marked:
            watermarked.write(Marked)

    print(f"Requested document has been watermarked and can be found at: {os.path.dirname(doc_file)}\\")


def generate(requester, attachment_path):
    # Create an email with an attachment
    attachment = os.path.splitext(attachment_path)[0] + "_watermarked.pdf"
    recipient = input("What is the email address of the requester? ")
    result = re.match(email_pattern, recipient)
    if not result:
        print("Please provide a valid email address.")
        generate(recipient, attachment_path)
    elif result:
        title = input("What is the subject of this email? ")
        message = email.message.EmailMessage()
        message["From"] = "junwonsuh@gmail.com"
        message["To"] = recipient
        message["Subject"] = title
        body = f"Here is the requested document {requester}. \nIf you look above each page, you will see 2 lines of texts; these are done for security measures. " \
               f"\nThe first line you see is the MD5 checksum of the PDF file, guaranteeing the integrity of the document, that nothing has been changed." \
               f"\nThe second line is the MD5 checksum, made by combining both the PDF and your name; both these checksums are very unique, allowing the  corporate to keep track of the " \
               f"potential leakage of data." \
               f"\n\n" \
               f"If you need another documents, please let me know." \
               f"\nHave a good day!" \
               f"\nSincerely," \
               f"\nJ. S." \

        message.set_content(body)

        if attachment_path != "":
            mime_type, _ = mimetypes.guess_type(attachment)
            mime_type, mime_subtype = mime_type.split('/', 1)

            with open(f"{attachment}", 'rb') as attach:
                message.add_attachment(attach.read(), maintype=mime_type, subtype=mime_subtype, filename=attachment)

        return message


def send_email(message, requester):
    while True:
        try:
        # with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as mail_server:
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as mail_server:
                mail_server.ehlo()
                mail_server.starttls() # mute if .SMTP_SSL
                mail_server.login('capstoneproject789@gmail.com', 'CapstoneProject#')
                mail_server.send_message(message)
                print("Email sent with the attachment")
                mail_server.quit()
        except Exception:
            print(f"Please copy & paste the following to the email manually along with the attachment file."
                  f"Here is the requested document {requester}.\nIf you look above each page, you will see 2 lines of texts; these are done for security measures."
                  f"\nThe first line you see is the MD5 checksum of the PDF file, guaranteeing the integrity of the document, that nothing has been changed."
                  f"\nThe second line is the MD5 checksum, made by combining both the PDF and your name; both these checksums are very unique, allowing the corporate to keep track of the "
                  f"potential leakage of any proprietary document."
                  f"\n\n"
                  f"If you need another documents, please let me know."
                  f"\nHave a good day!"
                  f"\nSincerely,"
                  f"\nJ. S.")
            sys.exit(1)


if __name__ == "__main__":
    main()
