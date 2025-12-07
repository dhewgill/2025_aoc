#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d3p1.txt" #r"data/d3p1_ex.txt"
P2_DATFILE = P1_DATFILE #r"data/d3p1_ex.txt"

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

    # Day 3, part 1.
    d3p1 = do_d3p1(P1_DATFILE)
    logging.info(f"Part 1: {d3p1}") # 

    # Day 3, part 2.
    # d3p2 = do_d3p2(P2_DATFILE)
    # logging.info(f"Part 2: {d3p2}") # 

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def get_joltage(bank_info: str, nmax:int = 2) -> int:
    max_vals = ""
    bank_info_list = [n for n in bank_info]
    max_val_ints = []
    # First, get the nmax largest values in the bank info.
    for _ in range(nmax):
        max_val = max(int(i) for i in bank_info_list)
        max_val_ints.append(max_val)
        bank_info_list.remove(str(max_val))

    # Then, run through the bank info and build the max_vals string.
    for b in bank_info:
        if int(b) in max_val_ints:
            max_vals += b
            max_val_ints.remove(int(b))
        if len(max_vals) >= nmax:
            break

    # for _ in range(nmax):
    #     max_val = max(int(i) for i in bank_info_list)
    #     max_vals += str(max_val)
    #     bank_info_list.remove(str(max_val))
    return int(max_vals)


def do_d3p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    total_joltage = 0
    for bank in raw_data:
        joltage = get_joltage(bank)
        logging.info("Bank: %s, Joltage: %d", bank, joltage)
        total_joltage += joltage

    return total_joltage


def do_d3p2(datafile: str) -> int:
    raw_data = parse_file(datafile)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
