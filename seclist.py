import xmltodict
import ipaddress


protocols = {
    "tcp": 6,
    "udp": 17
}

routing_flags = {
    "A": "active",
    "?": "loose",
    "C": "connect",
    "H": "host",
    "S": "static",
    "~": "internal",
    "R": "rip",
    "O": "ospf",
    "B": "bgp",
    "Oi": "ospf intra-area",
    "Oo": "ospf inter-area",
    "O1": "ospf ext-type-1",
    "O2": "ospf ext-type-2",
    "E": "ecmp",
    "M": "multicast",
}

def find_dest_routes(device, dest):
    print(f"[*] Finding routes to {dest}.\n")

    routes = xmltodict.parse(
        device.op("show routing route", xml=True)
    )

    possible_routes = []
    for route in routes['response']['result']['entry']:
        destination_network = ipaddress.ip_network(route['destination'])
        target_destination = ipaddress.ip_address(dest)

        if target_destination in destination_network:
            possible_routes.append(route)

    route_count = 1

    if possible_routes:
        for route in possible_routes:
            print(f'{route_count}. VR: {route["virtual-router"]}')
            print(f'Destination: {route["destination"]}')
            print(f'Next Hop: {route["nexthop"]}')
            print(f'Metric: {route["metric"]}')
            print(f'Interface: {route["interface"]}')
            flags = route['flags'].split()
            print("Flags:")
            for flag in flags:
                print(f'  - {routing_flags.get(flag)}')
            print()
            route_count += 1
    else:
        print(f"[!] No routes found to {dest}.")


def _excecute_check(device, args):
    src = args.source
    dst = args.destination
    proto = protocols.get(args.proto)
    port = args.port

    print(f"[*] Checking policies from {src} to {dst}.\n")

    policies = device.test_security_policy_match(source=src, destination=dst, protocol=proto, port=port)

    if policies:
        for policy in policies:
            print(f'{policy["index"]}. Name: {policy["name"]}')
            print(f'Action: {policy["action"]}')
            print()

        find_dest_routes(device=device, dest=dst)


def create_parser(parent_subparsers):
    description = "Firewall Security Policies Operations."
    parser = parent_subparsers.add_parser("seclist", help=description)

    subparsers = parser.add_subparsers(metavar="subcommand")
    subparsers.required = True

    check_description = "Test security policies based from source, destination, protocol, and port."
    check_parser = subparsers.add_parser("check", description=check_description, help=check_description)
    check_parser.add_argument("-s", "--source", required=True, help="Source IP Address.")
    check_parser.add_argument("-d", "--destination", required=True, help="Destination IP Address.")
    check_parser.add_argument("--proto", required=True, help="Destination protocol.", choices=["tcp", "udp"])
    check_parser.add_argument("--port", required=True, help="Destination port.")

    check_parser.set_defaults(execute=_excecute_check)