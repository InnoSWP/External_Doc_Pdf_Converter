import multiprocessing
import psutil
import sys
import argparse
from pathlib import Path
import os

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
	p = parser.parse_args()
	if p.processes is not None:
		proc_count = p.processes
	else:
		proc_count = os.cpu_count()
	conv_type = p.convtype
	infile_path_list = p.infiles
	infile_path_list.sort(key=lambda x: x.stat().st_size)  # Sort them according to filesize
	proc_count = min(proc_count, len(infile_path_list))
	worker_lists = [[] for i in range(proc_count)]
	for i in range(len(infile_path_list)):
		worker_lists[i % proc_count].append(infile_path_list[0].absolute())
		infile_path_list.pop(0)

	print(proc_count)
	print(worker_lists)


if __name__ == "__main__":
	main()
