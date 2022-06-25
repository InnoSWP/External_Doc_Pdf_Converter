import os
import arguments
import utils
import unoserver_worker
import multiprocessing
from itertools import repeat

UNOSERVER_PORT = 2002
# Callbacks
track_job = None
complete = None


def unoserver_convert(args: arguments.ConversionArguments):
    cur_server_count = utils.get_process_count("unoserver")
    for i in range(cur_server_count, args.proc_count):  # Create unoservers for parallelization,
        # if we don't have enough present already
        # This command creates a detached unoserver so that it doesn't shutdown when the script ends.
        os.system("nohup unoserver --port {} >/dev/null 2>&1 &".format(UNOSERVER_PORT + i))
    # We do not care about order, so we can use a pool of workers for conversion
    pool = multiprocessing.Pool(processes=args.proc_count,
                                initializer=lambda: unoserver_worker.initialize_converters(args))
    res = pool.starmap_async(unoserver_worker.convert_to_pdf, zip(args.input_paths, repeat(args.output_folder)),
                             chunksize=1, callback=complete)
    track_job(res)
    pool.close()
    pool.join()
    if args.kill:
        os.system("pkill unoserver")  # Kill all the servers if the kill flag is set
