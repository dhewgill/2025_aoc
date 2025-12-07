#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d2p1_ex.txt" #r"data/d2p1.txt" #r"data/d2p1_ex.txt"
P2_DATFILE = P1_DATFILE #r"data/d2p1_ex.txt"

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-lvl", dest="log_lvl", type=str, default="INFO", help="Logging level."
    )
    args = parser.parse_args()
    log_lvl = args.log_lvl

    log_fmt = "%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s:%(lineno)d: %(message)s"
    logging.basicConfig(
        level=log_lvl,
        format=log_fmt,
        datefmt="%Y-%m-%d,%H:%M:%S",
        handlers=(logging.StreamHandler(sys.stdout),),
    )

    print("Start\n")

    # Day 2, part 1.
    d2p1 = do_d2p1(P1_DATFILE)
    logging.info(f"Part 1: Secret code is {d2p1}") # 

    # Day 2, part 2.
    # d2p2 = do_d2p2(P2_DATFILE)
    # logging.info(f"Part 2: Secret code is {d2p2}") # 

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_input(raw_data: list[str]) -> list[tuple[int, int]]:
    parsed_data = []
    ranges = raw_data[0].split(",")
    for r in ranges:
        r_lo, r_hi = r.split("-")
        parsed_data.append((int(r_lo), int(r_hi)))

    return parsed_data


def do_d2p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    parsed_data = parse_input(raw_data)
    logging.info("Parsed data: %s", parsed_data)

    return None


def do_d2p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    parsed_data = parse_input(raw_data)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
