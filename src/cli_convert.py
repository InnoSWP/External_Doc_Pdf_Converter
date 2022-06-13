import argparse
from pathlib import Path
import os
import converters
import utils
import arguments


def parse_console_arguments():
	parser = argparse.ArgumentParser("Convert documents to pdf files")
	parser.add_argument("infiles", nargs="+", type=utils.validate_file, help="documents to convert")
	parser.add_argument("-p", "--processes", nargs="?", type=int, help="number of processes for parallelization")
	parser.add_argument("-ct", "--convtype", nargs="?", type=str, default="unoserver",
						help="conversion type, either \"msoffice\" or \"unoserver\"")
	parser.add_argument("-k", "--kill", action="store_true", help="kill convert server after conversion")
	parser.add_argument("-o", "--output-folder", type=Path, help="path where to store the converted documents")
	p = parser.parse_args()
	args = arguments.ConversionArguments()
	if p.processes is not None:
		args.proc_count = p.processes
	else:
		args.proc_count = os.cpu_count()  # Default to cpu count
	args.conv_type = p.convtype
	args.output_folder = p.output_folder
	args.input_paths = p.infiles
	args.kill = p.kill
	return args


def console_main():
	args = parse_console_arguments()
	if args.conv_type == "unoserver":
		converters.unoserver_convert(args)


if __name__ == "__main__":
	console_main()
