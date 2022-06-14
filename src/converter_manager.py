from enum import Enum
import time
import utils
import arguments
import unoserver_converter


class ConvertingMethod(Enum):
	UNOSERVER = 1
	DOCX4J = 2


CONVERSION_METHOD_STRING = {
	"unoserver": ConvertingMethod.UNOSERVER,
	"docx4j": ConvertingMethod.DOCX4J
}

DEFAULT_CONVERSION_METHOD = ConvertingMethod.UNOSERVER

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


def start_conversion(args: arguments.ConversionArguments):
	try:
		conversion_method: ConvertingMethod = CONVERSION_METHOD_STRING[args.conv_type]
	except KeyError:
		conversion_method: ConvertingMethod = DEFAULT_CONVERSION_METHOD
		print("Invalid conversion method specified, defaulting to {}".format(DEFAULT_CONVERSION_METHOD.name))
	global worker_total
	worker_total = len(args.input_paths)
	if conversion_method == ConvertingMethod.UNOSERVER:
		unoserver_converter.track_job = track_job
		unoserver_converter.complete = complete
		unoserver_converter.unoserver_convert(args)
	if conversion_method == ConvertingMethod.DOCX4J:
		pass  # Should be simple to add support for it, with the new structure

