import argparse
from pathlib import Path
import arguments
import utils


def parse_console_arguments() -> arguments.ConversionArguments:
    parser = argparse.ArgumentParser("Convert documents to pdf files")
    parser.add_argument("infiles", nargs="+", type=utils.validate_file, help="documents to convert")
    parser.add_argument("-p", "--processes", nargs="?", type=int, help="number of processes for parallelization")
    parser.add_argument("-ct", "--convtype", nargs="?", type=str, default="unoserver",
                        help="conversion type, either \"msoffice\" or \"unoserver\"")
    parser.add_argument("-k", "--kill", action="store_true", help="kill convert server after conversion")
    parser.add_argument("-o", "--output-folder", type=Path, help="path where to store the converted documents")
    p = parser.parse_args()
    args = arguments.ConversionArguments()
    args.conv_type = p.convtype
    args.output_folder = p.output_folder
    args.input_paths = p.infiles
    args.proc_count = p.processes
    args.kill = p.kill
    return args
