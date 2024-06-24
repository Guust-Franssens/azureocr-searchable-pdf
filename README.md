# Azure Document OCR
This repo walks you through how to create a searchable PDF from [Azure Form Recognizer OCR](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-ocr) using [pymupdf (aka fitz)](https://pymupdf.readthedocs.io/en/latest/index.html).

## Setup
Setup your virtual environment with the dependencies listed in the [environment.yml](environment.yml) using conda/mamba/... and [install the ipykernel](https://ipython.readthedocs.io/en/stable/install/kernel_install.html) if you want to use notebooks.

Then modify the [.env](.env) file to have your Azure OCR endpoint and key.

## Notebook
[The following notebook](searchable_pdf.ipynb) can help visualize how we overlay the text on the PDF. This can be handy if you want to adapt something and quickly see the results.

## Script
Executing it as a script `python -m searchable_pdf 1998-05-15_0057.pdf`