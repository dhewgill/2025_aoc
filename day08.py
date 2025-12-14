#!/usr/bin/env python

import argparse
import logging
import math
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d8p1_ex.txt" #r"data/d8p1_ex.txt"
P2_DATFILE =  P1_DATFILE #r"data/d8p1_ex.txt"

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
    d8p1 = do_d8p1(P1_DATFILE)
    logging.info(f"Part 1: {d8p1}") # 

    # Part 2.
    d8p2 = do_d8p2(P2_DATFILE)
    logging.info(f"Part 2: {d8p2}") # 


    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
class Node:
    def __init__(self, coords: tuple[int]) -> None:
        self._coords = coords
        self.x, self.y, self.z = self._coords

    def distance(self, other: 'Node') -> int:
        return math.sqrt(
            math.pow(self.x - other.x, 2)
            + math.pow(self.y - other.y, 2)
            + math.pow(self.z - other.z, 2)
        )

    def __repr__(self) -> str:
        return f"Node{self._coords}"


def parse_to_nodes(raw_data: list[str]) -> list[Node]:
    nodes = []
    for line in raw_data:
        coords = tuple(int(c) for c in line.split(","))
        nodes.append(Node(coords))
    return nodes


def do_d8p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    junction_boxes = parse_to_nodes(raw_data)
    logging.info("Parsed %d junction boxes.", junction_boxes)

    return None


def do_d8p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
