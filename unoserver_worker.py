import unoserver
import multiprocessing
from pathlib import Path
import subprocess


def convert_to_pdf(file_path: Path, server_port):
	worker_id = multiprocessing.current_process()._identity[0] - 1
	infile = str(file_path.absolute())
	outfile = str(file_path.absolute().parent) + "/" + file_path.absolute().stem + ".pdf"
	subprocess.Popen(["unoconvert", "--port", str(server_port + worker_id), infile, outfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
