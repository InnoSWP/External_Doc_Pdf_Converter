# Docx_To_Pdf
Convert DOCX to PDF on a local machine.

## Requirements
Requires LibreOffice and python3 (with pip) installed.
To install dependencies:

    sudo scripts/setup_environment

## Usage
    docx_to_pdf [-h] [-p [PROCESSES]] [-ct [CONVTYPE]] [-k] [-o [OUTPUT-FOLDER]] infiles [infiles ...]
- -p [PROCESSES], --processes [PROCESSES]: The number of processes to run in parallel for conversion. Defaults to the number of cores on the system.
- -ct [CONVTYPE], --convtype [CONVTYPE]: The conversion method used, either msoffice or unoserver. Defaults to "msoffice".
- -k, --kill: Kill the convert server after conversion.
- -o [OUTPUT-FOLDER], --output-folder [OUTPUT-FOLDER]: Directory where to store the converted documents.
- infiles: List of files to convert, which must end in .xls or .docx. .xls conversion works only with msoffice conversion method.

## Running server inside docker container
    rm -rf venv/
    docker build -t external_doc_pdf_converter .
    docker run -it -p 5000:5000 external_doc_pdf_converter

## 🔧 Technologies & Tools
![](https://img.shields.io/badge/OS-Linux-informational?style=flat&logo=linux&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Linter-SonarCloud-informational?style=flat&logo=SonarCloud&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Linter-SuperLinter-informational?style=flat&logo=Superlinter&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Server-Unoserver-informational?style=flat&logo=unoserver&logoColor=white&color=2bbc8a)
