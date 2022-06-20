import argument_processer
import cli_parser


def console_main():
    args = cli_parser.parse_console_arguments()
    argument_processer.process_arguments(args)


if __name__ == "__main__":
    console_main()
