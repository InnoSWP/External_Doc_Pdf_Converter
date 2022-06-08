from pathlib import Path
import psutil
import argparse


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