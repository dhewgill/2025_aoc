#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d5p1.txt" #r"data/d5p1_ex.txt"
P2_DATFILE =  P1_DATFILE #r"data/d5p1_ex.txt"

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

    # Day 4, part 1.
    d5p1 = do_d5p1(P1_DATFILE)
    logging.info(f"Part 1: {d5p1}") # 529

    # Day 4, part 2.
    d5p2 = do_d5p2(P2_DATFILE)
    logging.info(f"Part 2: {d5p2}") # 

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_input(raw_data: list[str]) -> tuple[list[object], list[int]]:
    parsed_ranges = []
    ingredients = []
    parse_ingredients = False
    for line in raw_data:
        if line.strip() == "":
            parse_ingredients = True
            continue
        if parse_ingredients:
            ingredients.append(int(line.strip()))
        else:
            range_parts = line.strip().split("-")
            range_start, range_end = range_parts
            parsed_ranges.append(range(int(range_start), int(range_end)+1))
    return (parsed_ranges, ingredients)


def do_d5p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    ranges, ingredients = parse_input(raw_data)
    logging.debug("Parsed ranges: %s, parsed ingredients: %s", ranges, ingredients)
    fresh_ingredients = []
    for i in ingredients:
        for r in ranges:
            if i in r:
                fresh_ingredients.append(i)
                logging.debug("Ingredient %d is in range %s", i, r)
                break
    return len(fresh_ingredients)


def do_d5p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
