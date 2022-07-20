#! /usr/bin/env python3 

import PyPDF2
from project import convert_doc, md5hash, name_hash, total_hash, watermarker_pdf, pdfMerger, generate, send_email
import sys
import re
import email
import mimetypes
import smtplib
import os
from docx2pdf import convert
import hashlib
from fpdf import FPDF
from getpass4 import getpass
# import mailslurp_client


doc = "C:\\Users\\junwo\\PycharmProjects\\NSAA\\Capstone\\test.docx"
# pdf = "C:\\Users\\junwo\\PycharmProjects\\NSAA\\Capstone\\test.pdf"
total_sum = total_hash(md5hash(doc), name_hash("Junwon Suh"))
pdf_read = open("C:\\Users\\junwo\\PycharmProjects\\NSAA\\Capstone\\test.pdf", 'rb').read()
pdf_read1 = open("C:\\Users\\junwo\\OneDrive\\Desktop\\test.docx", "rb").read()
name = "Junwon Suh"

def test_md5sum():
    assert md5hash(doc) == hashlib.md5(pdf_read).hexdigest()
    # assert md5sum(doc) != hashlib.md5(pdf_read1).hexdigest()


def test_total_hash():
    total = f"{hashlib.md5(pdf_read).hexdigest()}{hashlib.md5(name.encode()).hexdigest()}" # the latter is the md5sum of "Junwon Suh"
    assert total_hash(md5hash(doc), name_hash("Junwon Suh")) == hashlib.md5(total.encode()).hexdigest()


def test_convert_doc(): # should be gone?
    assert convert_doc(doc) != open(doc)
    assert convert_doc("C:\\Users\\junwo\\OneDrive\\Desktop\\test.docx") != open("C:\\Users\\junwo\\OneDrive\\Desktop\\test.docx")


def test_name_hash(): #this is good
    assert name_hash("Junwon Suh") == "7cab4e1d8bb5fb0fd0d62ee64eb9fb68"
    assert name_hash("John Christopher Depp") == "08fe91cfc1b297f8b0cc925044e96541"


def test_watermarker_pdf():
    new_doc = "C:\\Users\\junwo\\OneDrive\\Desktop\\test.docx"
    assert watermarker_pdf(doc_path=doc, pdf_md5=md5hash(doc), total_md5=total_sum, requester=name,
                           name_md5=name_hash(name)) != open(doc)
