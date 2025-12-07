#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d2p1.txt" #r"data/d2p1_ex.txt"
P2_DATFILE = r"data/d2p1_ex.txt"

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
    logging.info(f"Part 1: Secret code is {d2p1}") # 12586854255

    # Day 2, part 2.
    d2p2 = do_d2p2(P2_DATFILE)
    logging.info(f"Part 2: Secret code is {d2p2}") # 

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


def chunker(seq: list, size: int) -> list[list]:
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def find_invalid_ids(
    id_range: tuple[int, int], check_subs:bool = False
) -> list[int]:
    """
    Invalid IDs are those that are that contain a duplicated sequence of digits
    such as: 11, 1212, 123123, etc.
    """
    invalid_ids = []
    r_lo, r_hi = id_range

    for id_num in range(r_lo, r_hi + 1):
        id_str = str(id_num)
        id_len = len(id_str)

        if id_len == 1:
            continue
        if id_len % 2 != 0:
            if check_subs:
                if all(i == id_str[0] for i in id_str):
                    invalid_ids.append(id_num)
            continue

        half_len = id_len // 2
        first_half = id_str[0:half_len]
        second_half = id_str[half_len:id_len]
        if first_half == second_half:
            invalid_ids.append(id_num)
            continue

        if check_subs:
            for n in range(2, half_len):
                if id_len % n != 0:
                    continue
                subs = chunker(id_str, n)
                if all(s == subs[0] for s in subs):
                    invalid_ids.append(id_num)
                    break

    return invalid_ids


def do_d2p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    parsed_data = parse_input(raw_data)
    logging.debug("Parsed data: %s", parsed_data)
    invalid_id_sum = 0
    for id_range in parsed_data:
        invalid_ids = find_invalid_ids(id_range)
        logging.debug("Invalid IDs in range %s: %s", id_range, invalid_ids)
        invalid_id_sum += sum(invalid_ids)

    return invalid_id_sum


def do_d2p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    parsed_data = parse_input(raw_data)
    logging.debug("Parsed data: %s", parsed_data)
    invalid_id_sum = 0
    for id_range in parsed_data:
        invalid_ids = find_invalid_ids(id_range, True)
        logging.info("Invalid IDs in range %s: %s", id_range, invalid_ids)
        invalid_id_sum += sum(invalid_ids)

    return invalid_id_sum


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
