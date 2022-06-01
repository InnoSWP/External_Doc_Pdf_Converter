import multiprocessing
from itertools import repeat
import psutil
import argparse
from pathlib import Path
import os
import unoserver_worker
import time

UNOSERVER_PORT = 2002


def get_process_count(process_name):
	"""
	Check if there is any running process that contains the given name processName.
	"""
	# Iterate over the all the running process
	count = 0
	for proc in psutil.process_iter():
		try:
			# Check if process name contains the given name string.
			if process_name.lower() in proc.name().lower():
				count += 1
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return count


def validate_file(f):
	f = Path(f)
	if not f.exists():
		raise argparse.ArgumentTypeError("{0} does not exist".format(f))
	return f


def main():
	parser = argparse.ArgumentParser("Convert documents to pdf files")
	parser.add_argument("infiles", nargs="+", type=validate_file, help="documents to convert")
	parser.add_argument("-p", "--processes", nargs="?", type=int, help="number of processes for parallelization")
	parser.add_argument("-ct", "--convtype", nargs="?", type=str, default="unoserver",
						help="conversion type, either \"msoffice\" or \"unoserver\"")
	parser.add_argument("-k", "--kill", action="store_true", help="kill convert server after conversion")
	parser.add_argument("-o", "--output-folder", type=Path, help="path where to store the converted documents")
	p = parser.parse_args()
	if p.processes is not None:
		proc_count = p.processes
	else:
		proc_count = os.cpu_count()  # Default to cpu count
	conv_type = p.convtype
	output_path = p.output_folder
	infile_path_list = p.infiles
	supported_formats = [".docx", ".doc", ".xls", ".xlsx"]
	infile_path_list = list(filter(lambda x: x.suffix in supported_formats, infile_path_list))
	infile_path_list.sort(key=lambda x: x.stat().st_size)  # Sort them according to filesize
	proc_count = min(proc_count, len(infile_path_list))  # Don't make more workers than files to convert
	if conv_type == "unoserver":
		cur_server_count = get_process_count("unoserver")
		for i in range(cur_server_count, proc_count):  # Create unoservers for parallelization, if we don't have enough present already
			os.system("nohup unoserver --port {} >/dev/null 2>&1 &".format(UNOSERVER_PORT + i))  # This command creates a detached unoserver so that it doesn't shutdown when the script ends.
		if cur_server_count != proc_count:
			time.sleep(1)  # We need to do this because unoserver does not start immediately, and so if we don't wait a short bit, the converters may throw an error.
							# Should probably find a way to be able to tell when the server is working.
		pool = multiprocessing.Pool(processes=proc_count)  # We do not care about order, so we can use a pool of workers for conversion
		pool.starmap(unoserver_worker.convert_to_pdf, zip(infile_path_list, repeat(UNOSERVER_PORT), repeat(output_path)))
		if p.kill:
			os.system("pkill unoserver")  # Kill all the servers if the kill flag is set


if __name__ == "__main__":
	main()
