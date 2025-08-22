import yaml


def credential_handler(file):
    with open(file, "r") as f:
        data = yaml.safe_load(f)

    return data
