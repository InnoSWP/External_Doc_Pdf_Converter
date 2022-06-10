import os
import unoserver_worker
import time
import multiprocessing
from itertools import repeat
import utils
UNOSERVER_PORT = 2002


def unoserver_convert(port, proc_count, conv_type, output_path, infile_path_list, pkill):
	supported_formats = [".docx", ".doc", ".xls", ".xlsx"]
	infile_path_list = list(filter(lambda x: x.suffix in supported_formats, infile_path_list))
	infile_path_list.sort(key=lambda x: x.stat().st_size)  # Sort them according to filesize
	proc_count = min(proc_count, len(infile_path_list))  # Don't make more workers than files to convert
	cur_server_count = utils.get_process_count("unoserver")
	for i in range(cur_server_count, proc_count):  # Create unoservers for parallelization, if we don't have enough present already
		os.system("nohup unoserver --port {} >/dev/null 2>&1 &".format(port + i))  # This command creates a detached unoserver so that it doesn't shutdown when the script ends.
	if cur_server_count != proc_count:
		time.sleep(1)  # We need to do this because unoserver does not start immediately, and so if we don't wait a short bit, the converters may throw an error.
						# Should probably find a way to be able to tell when the server is working.
	pool = multiprocessing.Pool(processes=proc_count, initializer=unoserver_worker.initializeConverters)  # We do not care about order, so we can use a pool of workers for conversion
	pool.starmap(unoserver_worker.convert_to_pdf, zip(infile_path_list, repeat(port), repeat(output_path)))
	if pkill:
		os.system("pkill unoserver")  # Kill all the servers if the kill flag is set
