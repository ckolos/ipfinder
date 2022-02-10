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

            """
            We could use ips.extend() vs. append. This would result
            in a flat list vs. a list of lists. I'm keeping this as is as a reminder
            of the 'correct' way to flatten a list of lists and get uniq items
            """
            ips.append(find_ips(path))
    """
    This comprehension replaces the following code:
    for list in ips:
        for item in list:
            some_list = item

    uniq_ips = dict()
    for ip in some_list:
        uniq_ips[ip] = uniq.get(ip,0)+1
    print(sorted(uniq_ips.keys()))

    """
    [print(f"{x}") for x in sorted(set([x for y in ips for x in y].copy()))]


if __name__ == "__main__":
    main()
