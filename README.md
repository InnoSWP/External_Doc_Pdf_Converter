# 📚 Project Description
Convert DOCX to PDF on a local machine.

## 🎬 Demo

![Teaser](https://imgur.com/LpGefCM.gif)

## 📝 Usage
    docx_to_pdf [-h] [-p [PROCESSES]] [-ct [CONVTYPE]] [-k] [-o [OUTPUT-FOLDER]] infiles [infiles ...]
- -p [PROCESSES], --processes [PROCESSES]: The number of processes to run in parallel for conversion. Defaults to the number of cores on the system.
- -ct [CONVTYPE], --convtype [CONVTYPE]: The conversion method used, currently only unoserver. Defaults to "unoserver".
- -k, --kill: Kill the convert server after conversion.
- -o [OUTPUT-FOLDER], --output-folder [OUTPUT-FOLDER]: Directory where to store the converted documents.
- infiles: List of files to convert, which must end in .xls or .docx. .xls conversion works only with msoffice conversion method.

```
start_server
```
 - Starts the flask server.

## ✏️ Features

| Feature                                      | Supported |
|----------------------------------------------|:---------:|
| converting .doc files                        |     ✅     |
| converting .xls files                        |     ✅     |
| sending multiple files                       |     ✅     |
| converting with different languages texts    |     ✅     |
| converting of files with different encodings |     ✅     |
| returning status codes                       |     ✅     |

1) Install the requirements
1a) Optionally, install all the fonts that will be used in conversions.
2a) If you want to run the converter as CLI tool, just use it using docx_to_pdf script, it will create the virtual environment on the first start.
2b) If you want to run the converter as a server, just run start_server and wait until it loads.
2c) Additionally, you can run the server as a docker converter, see the next section for details.

## 🐳 Running server inside docker container
    rm -rf venv/
    docker build -t external_doc_pdf_converter .
    docker run -d -p <desired_port>:5000 external_doc_pdf_converter

## 🎛️ Requirements
Requires LibreOffice and python3 (with pip) installed.
To install dependencies:

    sudo scripts/setup_environment

## 🔧 Technologies & Tools
![OS Linux](https://img.shields.io/badge/OS-Linux-informational?style=flat&logo=linux&logoColor=white&color=2bbc8a)
![Code Python](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=2bbc8a)
![Linter SonarCloud](https://img.shields.io/badge/Linter-SonarCloud-informational?style=flat&logo=SonarCloud&logoColor=white&color=2bbc8a)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_External_Doc_Pdf_Converter&metric=bugs)](https://sonarcloud.io/summary/new_code?id=InnoSWP_External_Doc_Pdf_Converter)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_External_Doc_Pdf_Converter&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=InnoSWP_External_Doc_Pdf_Converter)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_External_Doc_Pdf_Converter&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=InnoSWP_External_Doc_Pdf_Converter)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_External_Doc_Pdf_Converter&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=InnoSWP_External_Doc_Pdf_Converter)
