import multiprocessing
from pathlib import Path
import subprocess


def convert_to_pdf(file_path: Path, base_server_port, out_path: Path = None):
	"""
	:param file_path: Path to the document to be converted
	:param base_server_port: Server port of the first unoserver
	:param out_path: Directory where to store the converted document
	"""
	worker_id = multiprocessing.current_process()._identity[0] - 1
	infile = str(file_path.absolute())
	if out_path is not None:
		outfile = str(out_path.absolute()) + ("/" if str(out_path.absolute())[-1] != "/" else "") + file_path.absolute().stem + ".pdf"
	else:
		outfile = str(file_path.absolute().parent) + "/" + file_path.absolute().stem + ".pdf"
	print(outfile)
	subprocess.Popen(["unoconvert", "--port", str(base_server_port + worker_id), infile, outfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
