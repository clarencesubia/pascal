# PASCAL

## Description
Palo Alto NGFW Synthesis, Collection, Automation, and Logging.

## Install python packages
```
pip3 install -r requirements.txt
```

## Install pascal_app package locally
```
pip3 install -e .
```

## Retrieve API key
```
curl -Hk "Content-Type: application/x-www-form-urlencoded" -X POST https://<IP ADDRESS>/api/?type=keygen -d 'user=<USER>&password=<PASSWORD>'
```

## Setup credentials file in YAML format
```
user: "<USER>"
api_key: "<API KEY>"
```

## Usage
- Health Checks
```
python3 pascal.py --firewall 192.168.227.100 --credentials credentials.yaml health-check check --target [sysinfo | ha | util | interface | vpn | license | all]
```

- Security Lists
```
python3 pascal.py --firewall 192.168.227.100 --credentials credentials.yaml seclist check -s <SOURCE IP> -d <DESTINATION IP> --proto [tcp | udp] --port <DESTINATION PORT>
```

# Author
Clarence R. Subia

