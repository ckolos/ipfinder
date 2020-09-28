#!/usr/bin/env python3

import ipaddress
import os
import re

import click

maybe_ip_addr = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
ips = list()


def is_ip(text):
    try:
        if ipaddress.ip_address(text):
            return text
    except ValueError:
        pass


def find_ips(file):
    with open(f"{file}") as f:
        matched = [x for x in maybe_ip_addr.findall(f.read()) if is_ip(x)]

    return matched


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("this_dir", type=click.Path(exists=True), nargs=1, required=True)
def main(this_dir):
    for dirpath, dirnames, filenames in os.walk(this_dir):
        for name in filenames:
            path = os.path.join(dirpath, name)
            ips.append(find_ips(path))

    [print(f"{x}") for x in sorted(set([x for y in ips for x in y].copy()))]


if __name__ == "__main__":
    main()
