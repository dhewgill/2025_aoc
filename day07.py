#!/usr/bin/env python

import argparse
from functools import lru_cache
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d7p1.txt" #r"data/d7p1_ex.txt"
P2_DATFILE =  P1_DATFILE #r"data/d7p1_ex.txt"

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

    # Part 1.
    d7p1 = do_d7p1(P1_DATFILE)
    logging.info(f"Part 1: {d7p1}") # 1615

    # Part 2.
    d7p2 = do_d7p2(P2_DATFILE)
    logging.info(f"Part 2: {d7p2}") # 43560947406326


    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def count_tachyon_splits(manifold: list[str]) -> int:
    # Track tachyon beams with a set storing their (row, col) locations.
    # A set is used because there may be overlapping beams.
    tachyon_beam_locs = set()
    split_count = 0
    max_rows = len(manifold) - 1
    #max_cols = len(manifold[0]) - 1
    for row, val in enumerate(manifold):
        if "S" in val:
            tachyon_beam_locs.add((row + 1, val.index("S")))
            continue
        if row == max_rows:
            continue

        for col, _ in enumerate(val):
            if (row, col) in tachyon_beam_locs:
                # Remove current tachyon beam from list - no longer needed.
                tachyon_beam_locs.remove((row, col))
                # Check row below to see if split needed.
                if manifold[row + 1][col] == "^":
                    split_count += 1
                    # Split tachyon beam to left and right of splitter.
                    tachyon_beam_locs.add((row + 1, col - 1))
                    tachyon_beam_locs.add((row + 1, col + 1))
                else: # Continue straight down.
                    tachyon_beam_locs.add((row + 1, col))

    return split_count


def in_bounds(manifold: list[str], beam_loc: tuple[int, int]) -> bool:
    row, col = beam_loc
    return (0 <= row < len(manifold)) and (0 <= col < len(manifold[0]))


@lru_cache()
def count_tachyon_timelines(manifold: tuple[str], beam_loc: tuple[int, int]) -> int:
    row, col = beam_loc
    if row == len(manifold) - 1:
        return 1

    if manifold[row + 1][col] == "^":
        left = (row + 1, col - 1)
        right = (row + 1, col + 1)
        left_count = 0
        right_count = 0
        if in_bounds(manifold, left):
            left_count = count_tachyon_timelines(manifold, left)
        if in_bounds(manifold, right):
            right_count = count_tachyon_timelines(manifold, right)
        return left_count + right_count

    return count_tachyon_timelines(manifold, (row + 1, col))


def do_d7p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    num_splits = count_tachyon_splits(raw_data)
    logging.debug("Number of tachyon splits: %d", num_splits)

    return num_splits


def do_d7p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    num_timelines = 1
    # Get the starting location of the tachyon beam.
    for row, val in enumerate(raw_data):
        if "S" in val:
            beam_loc = (row + 1, val.index("S"))
            break
    logging.debug("Tachyon beam starting location: %s", beam_loc)
    num_timelines = count_tachyon_timelines(tuple(r for r in raw_data), beam_loc)

    return num_timelines


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
