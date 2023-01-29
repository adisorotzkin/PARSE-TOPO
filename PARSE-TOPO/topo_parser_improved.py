import re
from time import sleep
from args_parser import arg_parser
from tqdm.auto import tqdm

sysimgguid_pattern = r"sysimgguid=(.*)"
hostguid_pattern = r"(?:switchguid|caguid)\=(.*)"
connection_pattern = r"\[([\d]+)\][\s]?([^\[]*)\[([\d]+)\]"


def main():
    args = arg_parser()
    parse_topology(args.path, args.print)

def parse_topology(path: str, print_chunk:bool):
    """
    The function that parses the topology file.
    In this case, the function will parse each chunk and right after that will print the result.
    That way, if the data is heavy, the user will already see some results without waiting.
    In addition, a progress bar was added.
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

    with tqdm(splitted_data,desc="Parsing progress",total=len(splitted_data)) as pbar:
        for chunk in splitted_data:
            hostguids = re.findall(hostguid_pattern, chunk)

            if len(hostguids) == 0: #empty list
                continue

            hostguid = hostguids[0]
            sysimgguid = re.findall(sysimgguid_pattern, chunk)[0]
            metadata[hostguid] = sysimgguid
            connections[hostguid] = {}
            all_connections = re.findall(connection_pattern, chunk)

            for connection in all_connections:
                host = connection[1].replace(' \t', '')
                src_port = connection[0]
                dst_port = connection[2]
                connections[hostguid][host] = (src_port, dst_port)
            
            pbar.update(1) #update the progress bar
            
            if print_chunk:
                print("Host:")
                print("sysimgguid="+metadata[hostguid])
                for item in connections[hostguid].items():
                    string_to_print = parse_remote_host(item)
                    print(string_to_print)
                    print("\n")
                pbar.refresh()
               

        print("Finished Parsing Topology File")

def parse_remote_host(host):
    if ("S" in host[0]):
        remote_host = "0x" + \
            host[0].replace("\"", '').split("-")[1].replace("000", "")
        return f"Connected to switch: switchguid={remote_host}, port={host[1][1]}"
    else:
        remote_host = host[0].replace("\"", '').split('-')[1]
        return f"Connected to host: caguid=0x{remote_host}, port={host[1][1]}"


if __name__ == "__main__":
    main()