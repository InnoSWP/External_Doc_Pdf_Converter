import multiprocessing
from pathlib import Path
import unoserver.converter
import unoserver_converter
import converter_manager

converter = None


def initialize_converters():
    # After the converter creates the workers, if the entire program hasn't stopped working (for example - web converter
    # then the ._identity[0] of the workers will keep going up and up, so we need to account for that.
    worker_id = multiprocessing.current_process()._identity[0] - 1 - converter_manager.workers_created
    global converter
    while True:
        try:
            converter = unoserver.converter.UnoConverter("127.0.0.1", unoserver_converter.UNOSERVER_PORT + worker_id)
        except BaseException as err:
            pass
        if converter is not None:
            break


def convert_to_pdf(file_path: Path, out_path: Path = None):
    """
    :param file_path: Path to the document to be converted
    :param base_server_port: Server port of the first unoserver
    :param out_path: Directory where to store the converted document
    """
    infile = str(file_path.absolute())
    if out_path is not None:
        outfile = str(out_path.absolute()) + (
            "/" if str(out_path.absolute())[-1] != "/" else "") + file_path.absolute().stem + ".pdf"
    else:
        outfile = str(file_path.absolute().parent) + "/" + file_path.absolute().stem + ".pdf"
    # print(outfile)
    try:
        converter.convert(inpath=infile, outpath=outfile, convert_to="pdf")
    except BaseException as err:
        print("Failed to convert {}".format(infile))
