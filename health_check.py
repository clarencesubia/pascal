import json
import xmltodict

def sys_info(device):
    print("--> System information check...\n")
    info = xmltodict.parse(
        device.op("show system info", xml=True)
    )
    
    system = info["response"]["result"]["system"]
    
    print(f"Hostname: {system['hostname']}")
    print(f"Management IP: {system['ip-address']}")
    print(f"Uptime: {system['uptime']}")
    print(f"Model: {system['model']}")
    print(f"Operational Mode: {system['operational-mode']}")
    print(f"Certificate Status: {system['device-certificate-status']}")
    print()


def ha_info(device):
    print("--> High availability check...\n")
    ha = xmltodict.parse(
        device.op("show high-availability all", xml=True)
    )

    ha_status = ha["response"]["result"]
    print(f"Enabled: {ha_status['enabled']}")
    print(f"Mode: {ha_status['group']['mode']}")
    print(f"Local Firewall Status:")
    print(f"State: {ha_status['group']['local-info']['state']}")
    print(f"HA1 IP Address: {ha_status['group']['local-info']['ha1-ipaddr']}")

    print(f"Peer Firewall Status:")
    print(f"State: {ha_status['group']['peer-info']['conn-ha1']['conn-status']}")
    print(f"State Reason: {ha_status['group']['peer-info']['conn-ha1']['conn-down-reason']}")
    print(f"HA1 IP Address: {ha_status['group']['peer-info']['ha1-ipaddr']}")
    print()


def interface(device):
    print("Under construction")


def vpn(device):
    print("Under construction")


def license(device):
    print("Under construction")


def _excecute_health_check(device, args):
    print("[*] Performing health checks...\n")

    if args.target == "sysinfo":
        sys_info(device=device)
    elif args.target == "ha":
        ha_info(device=device)
    elif args.target == "interface":
        interface(device=device)
    elif args.target == "vpn":
        vpn(device=device)
    elif args.target == "license":
        license(device=device)

    elif args.target == "all":
        sys_info(device=device)
        ha_info(device=device)


def create_parser(parent_subparsers):
    description = "Firewall Health Checks."
    parser = parent_subparsers.add_parser("health-check", help=description)

    subparsers = parser.add_subparsers(metavar="subcommand")
    subparsers.required = True

    check_description = "Check status of various firewall resources."
    check_parser = subparsers.add_parser("check", description=check_description, help=check_description)
    check_parser.add_argument("--target", required=True, help="Health check firewall resources.")

    check_parser.set_defaults(execute=_excecute_health_check)