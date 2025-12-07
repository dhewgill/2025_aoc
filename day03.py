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
    logging.info(f"Part 1: {d3p1}") # 17343

    # Day 3, part 2.
    # d3p2 = do_d3p2(P2_DATFILE)
    # logging.info(f"Part 2: {d3p2}") # 

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def get_joltage(bank_info: str, nmax:int = 2) -> int:
    """
    Find the max and then then keep finding the max of the remaining digits in the
    substring starting at index max.
    """
    bank_info_list = [n for n in bank_info]
    joltage_str = ""
    max_val = max(int(n) for n in bank_info_list)
    logging.debug("Initial max joltage: %d", max_val)

    # Check for pathological case where the max is at the end of the string.
    if bank_info_list.index(str(max_val)) == len(bank_info_list) - 1:
        max_val = max(int(n) for n in bank_info_list[:-1])
        logging.debug("Adjusted initial max joltage: %d", max_val)

    for _ in range(nmax):
        joltage_str += str(max_val)
        # Find the index of max_val in bank_info_list.
        max_idx = bank_info_list.index(str(max_val))
        logging.debug("Max joltage: %d at index %d", max_val, max_idx)
        # Remove all digits before and including max_idx from bank_info_list and bank_info_ints.
        bank_info_list = bank_info_list[max_idx + 1 :]
        if bank_info_list:
            max_val = max(int(n) for n in bank_info_list)

    return int(joltage_str)


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
