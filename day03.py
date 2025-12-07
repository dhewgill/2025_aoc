#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d3p1.txt" #r"data/d3p1_ex.txt"
P2_DATFILE =  P1_DATFILE #r"data/d3p1_ex.txt"

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
    d3p2 = do_d3p2(P2_DATFILE)
    logging.info(f"Part 2: {d3p2}") # 172664333119298

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def get_joltage(bank_info: str, nmax:int = 2) -> int:
    joltage_str = ""
    remaining_info = bank_info
    n_remain = nmax
    sorted_digits = sorted(set(bank_info), reverse=True)
    for _ in range(nmax):
        for d in sorted_digits:
            if d in remaining_info:
                idx = remaining_info.index(str(d))
                logging.debug("Found digit %s at index %d", d, idx)
                if idx <= len(remaining_info) - n_remain:
                    joltage_str += str(d)
                    remaining_info = remaining_info[idx + 1 :]
                    n_remain -= 1
                    break
    return int(joltage_str)


def do_d3p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    total_joltage = 0
    for bank in raw_data:
        #joltage = get_joltage(bank)
        joltage = get_joltage(bank)
        logging.debug("Bank: %s, Joltage: %d", bank, joltage)
        total_joltage += joltage

    return total_joltage


def do_d3p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    total_joltage = 0
    for bank in raw_data:
        joltage = get_joltage(bank, 12)
        logging.debug("Bank: %s, Joltage: %d", bank, joltage)
        total_joltage += joltage

    return total_joltage


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
