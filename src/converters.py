import os
import unoserver_worker
import time
import multiprocessing
from itertools import repeat
import utils
UNOSERVER_PORT = 2002
worker_progress = 0
worker_total = 0


def track_job(job, update_interval=0.1):
	"""
	Tracks an async job
	:param job: Return of async pool function
	:param update_interval: How frequently to update progress
	"""
	global worker_progress
	global worker_total
	while job._number_left > 0:
		worker_progress = worker_total - job._number_left * job._chunksize
		print_cur_progress()
		time.sleep(update_interval)


def print_cur_progress():
	utils.printProgressBar(worker_progress, worker_total, prefix="Conversion progress: ", print_end="\r")


def complete(result):
	global worker_progress
	worker_progress = worker_total
	print_cur_progress()


def unoserver_convert(port, proc_count, conv_type, output_path, infile_path_list, pkill):
	supported_formats = [".docx", ".doc", ".xls", ".xlsx"]
	infile_path_list = list(filter(lambda x: x.suffix in supported_formats, infile_path_list))
	infile_path_list.sort(key=lambda x: x.stat().st_size)  # Sort them according to filesize
	global worker_total
	worker_total = len(infile_path_list)
	proc_count = min(proc_count, len(infile_path_list))  # Don't make more workers than files to convert
	cur_server_count = utils.get_process_count("unoserver")
	for i in range(cur_server_count, proc_count):  # Create unoservers for parallelization, if we don't have enough present already
		os.system("nohup unoserver --port {} >/dev/null 2>&1 &".format(port + i))  # This command creates a detached unoserver so that it doesn't shutdown when the script ends.
	pool = multiprocessing.Pool(processes=proc_count, initializer=unoserver_worker.initialize_converters)  # We do not care about order, so we can use a pool of workers for conversion
	res = pool.starmap_async(unoserver_worker.convert_to_pdf, zip(infile_path_list, repeat(output_path)), chunksize=1, callback=complete)
	track_job(res)
	pool.close()
	pool.join()
	if pkill:
		os.system("pkill unoserver")  # Kill all the servers if the kill flag is set
