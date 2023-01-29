import argparse

def arg_parser():
    parser = argparse.ArgumentParser(
        prog="python topo_parser.py",
        description='This program parses and prints the topology of an ib network based on topology discovery tool output files.',
        epilog='To start, run python topo_parser.py -f [file path]')
    parser.add_argument(
        "-f", "--file", help="Path to the relevant file", type=str, dest="path", required=True)
    parser.add_argument(
        "-p", "--print", help="Print parsed topology", action='store_true')

    args = parser.parse_args()
    return args