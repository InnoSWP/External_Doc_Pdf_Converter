# Usage
    doc_to_pdf [-h] [-p [PROCESSES]] [-ct [CONVTYPE]] infiles [infiles ...]
 - -p [PROCESSES]: The number of processes to run in parallel for conversion. Defaults to the number of cores on the system.
 - -ct [CONVTYPE]: The conversion method used, either msoffice or unoserver. Defaults to "msoffice".
 - infiles: List of files to convert, which must end in .xls or .docx. .xls conversion works only with msoffice conversion method.

