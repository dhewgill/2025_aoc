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
    logging.info(f"Part 2: {d5p2}") # 344260049617193


    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_input(raw_data: list[str]) -> tuple[list[range], list[int]]:
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


def get_overlap_range(r1: range, r2: range) -> range | None:
    start = max(r1.start, r2.start)
    end = min(r1.stop, r2.stop)
    if start < end:
        return range(start, end)
    return None


def consolidate(r1: range, r2: range) -> range:
    """
    Consolidate two ranges known to overlap.
    """
    new_start = min(r1.start, r2.start)
    new_end = max(r1.stop, r2.stop)
    return range(new_start, new_end)


def consolidate_ranges(ranges: list[range]) -> list[range]:
    """
    Consolidate a list of ranges that may have overlaps into a list of non-overlapping ranges.
    """
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    consolidated = []
    for r in sorted_ranges:
        if not consolidated:
            consolidated.append(r)
            continue

        last_r = consolidated[-1]
        overlap_range = get_overlap_range(last_r, r)
        if overlap_range is not None:
            # Merge ranges.
            new_range = consolidate(last_r, r)
            consolidated[-1] = new_range

        else:
            consolidated.append(r)

    return consolidated


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

    ranges, _ = parse_input(raw_data)
    logging.debug("Parsed ranges: %s", ranges)

    consolidated_ranges = consolidate_ranges(ranges)
    logging.debug("Consolidated ranges: %s", consolidated_ranges)
    return sum(len(r) for r in consolidated_ranges)


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
