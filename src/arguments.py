class ConversionArguments:
    def __init__(self, input_paths=None, proc_count=None, conv_type=None, kill=None, output_folder=None):
        self.input_paths = input_paths
        self.proc_count = proc_count
        self.conv_type = conv_type
        self.kill = kill
        self.output_folder = output_folder
