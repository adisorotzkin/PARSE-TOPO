import re
from args_parser import arg_parser

sysimgguid_pattern = r"sysimgguid=(.*)"
hostguid_pattern = r"(?:switchguid|caguid)\=(.*)"
connection_pattern = r"\[([\d]+)\][\s]?([^\[]*)\[([\d]+)\]"


def main():
    args = arg_parser()
    connections, metadata = parse_topology(args.path)
    if (args.print):
        print_topology(connections, metadata)


def parse_topology(path: str):
    """
    The function that parses the topology file.
    Args:
        path (str): path to file

    Returns:
        connections (dict): a dictionary that describes for each host its connections.
        metadata (dict): a dictionary with hostguid as key and sysimgguid as value.
    """
    connections = {} # a dict describing all connections
    metadata = {} # a dict describing the match between hostguid and sysimgguid

    with open(path, "r") as f:
        data = f.read()

    splitted_data = data.split("\n\n")

    for chunk in splitted_data:
        hostguid = re.findall(hostguid_pattern, chunk)

        if len(hostguid) == 0: #empty list
            continue

        hostguid = hostguid[0]
        sysimgguid = re.findall(sysimgguid_pattern, chunk)[0]
        metadata[hostguid] = sysimgguid
        connections[hostguid] = {}
        all_connections = re.findall(connection_pattern, chunk)

        for connection in all_connections:
            host = connection[1].replace(' \t', '')
            src_port = connection[0]
            dst_port = connection[2]
            connections[hostguid][host] = (src_port, dst_port)

    print("Finished Parsing Topology File")
    return connections, metadata


def parse_remote_host(host: list):
    if ("S" in host[0]):
        remote_host = "0x" + \
            host[0].replace("\"", '').split("-")[1].replace("000", "")
        return f"Connected to switch: switchguid={remote_host}, port={host[1][1]}"
    else:
        remote_host = host[0].replace("\"", '').split('-')[1]
        return f"Connected to host: caguid=0x{remote_host}, port={host[1][1]}"


def print_topology(connections: dict, metadata: dict):
    print("### Topology ###\n")
    for obj in connections.items():
        host = obj[0]
        all_cons = obj[1]
        print("Host:")
        print("sysimgguid="+metadata[host])
        for item in all_cons.items():
            string_to_print = parse_remote_host(item)
            print(string_to_print)
        print("\n")


if __name__ == "__main__":
    main()