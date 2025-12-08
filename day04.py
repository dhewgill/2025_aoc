#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d4p1.txt" #r"data/d4p1_ex.txt"
P2_DATFILE =  P1_DATFILE #r"data/d4p1_ex.txt"

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
    d4p1 = do_d4p1(P1_DATFILE)
    logging.info(f"Part 1: {d4p1}") # 

    # Day 4, part 2.
    d4p2 = do_d4p2(P2_DATFILE)
    logging.info(f"Part 2: {d4p2}") # 

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def print_grid(grid: list[str]) -> None:
    logging.info("Grid:")
    for row in grid:
        print(row)


def count_neigbbours(grid: list[str], row:int, col:int, occupied:str = "@") -> int:
    n_rows = len(grid)
    n_cols = len(grid[0])
    deltas = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]
    n_occupied = 0
    for dr, dc in deltas:
        r = row + dr
        c = col + dc
        if 0 <= r < n_rows and 0 <= c < n_cols:
            if grid[r][c] == occupied:
                n_occupied += 1

    return n_occupied


def parse_input(raw_data: list[str]) -> list[str]:
    parsed_data = []
    for line in raw_data:
        parsed_data.append(line.strip())
    return parsed_data


def do_d4p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    grid = parse_input(raw_data)
    #print_grid(grid)

    num_moveable = 0
    n_cols = len(grid[0]) # Assume all rows same length.
    for row_num, row in enumerate(grid):
        for col in range(n_cols):
            if row[col] != "@":
                continue
            n_occupied = count_neigbbours(grid, row_num, col)
            logging.debug("Cell (%d, %d) has %d occupied neighbours", row_num, col, n_occupied)
            if n_occupied < 4:
                num_moveable += 1
    return num_moveable


def do_d4p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
