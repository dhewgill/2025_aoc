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

    # Day 2, part 1.
    d3p1 = do_d3p1(P1_DATFILE)
    logging.info(f"Part 1: Secret code is {d3p1}") # 

    # Day 2, part 2.
    # d3p2 = do_d3p2(P2_DATFILE)
    # logging.info(f"Part 2: Secret code is {d3p2}") # 

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def get_joltage(bank_info: list[str], nmax:int = 2) -> int:
    pass

def do_d3p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.info("Raw data: %s", raw_data)

    return None


def do_d3p2(datafile: str) -> int:
    raw_data = parse_file(datafile)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
