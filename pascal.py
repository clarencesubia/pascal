#!/usr/bin/env python3

import sys
import argparse

import seclist
from credential_handler import credential_handler

from panos.base import PanDevice

parser = argparse.ArgumentParser(description="PA Synthesis, Collection, Automation, and Logging")
parser.add_argument("--firewall", required=True, help="Firewall hostname or IP address.")
parser.add_argument("--credentials", required=False, help="Credentials file containing user and api key.")

subparsers = parser.add_subparsers(metavar="command")
subparsers.required = True

seclist.create_parser(subparsers)

args = parser.parse_args()

firewall = args.firewall
creds_file = args.credentials

credentials = credential_handler(creds_file)
user = credentials["user"]
api_key = credentials["api_key"]

device = PanDevice(hostname=args.firewall, api_username=user, api_key=api_key)

cmd_result = args.execute(device, args)
exit_code = 0 if cmd_result or cmd_result is None else 1
sys.exit(exit_code)