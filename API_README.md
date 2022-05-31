# Usage
    doc_to_pdf [-h] [-p [PROCESSES]] [-ct [CONVTYPE]] [-k] infiles [infiles ...]
 - -p [PROCESSES], --processes [PROCESSES]: The number of processes to run in parallel for conversion. Defaults to the number of cores on the system.
 - -ct [CONVTYPE], --convtype [CONVTYPE]: The conversion method used, either msoffice or unoserver. Defaults to "msoffice".
 - -k, --kill: Kill the convert server after conversion.
 - infiles: List of files to convert, which must end in .xls or .docx. .xls conversion works only with msoffice conversion method.

