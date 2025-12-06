#!/usr/bin/env python

import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d1p1.txt" #r"data/d1p1_ex.txt"
P2_DATFILE = P1_DATFILE #r"data/d1p1_ex.txt"

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

    # Day 1, part 1.
    secret_code = do_d1p1(P1_DATFILE)
    logging.info(f"Part 1: Secret code is {secret_code}") # 1007

    # Day 1, part 2.
    secret_code = do_d1p2(P2_DATFILE)
    logging.info(f"Part 2: Secret code is {secret_code}") # 5820

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_input(raw_data: list[str]) -> list[tuple[str, int]]:
    parsed_data = []
    data_re = re.compile(r"^([L|R]+)(\d+)$")
    for line in raw_data:
        m = data_re.match(line)
        if m:
            turn_dir = m.group(1)
            steps = int(m.group(2))
            parsed_data.append((turn_dir, steps))

    return parsed_data


def get_new_position(
    current_pos: int, instruction: tuple[str, int], bounds: tuple[int, int],
) -> tuple[int, int]:
    min_bound, max_bound = bounds
    turn_dir, steps = instruction
    num_wraps = steps // (max_bound + 1)
    new_steps = steps % (max_bound + 1)

    if turn_dir == "R":
        new_pos = current_pos + new_steps
    elif turn_dir == "L":
        new_pos = current_pos - new_steps
    else:
        raise ValueError(f"Invalid turn direction: {turn_dir}")

    if (
        current_pos != 0
        and (new_pos != max_bound + 1)
        and ((new_pos < min_bound) or (new_pos > max_bound))
    ):
        num_wraps += 1

    # Map new position within bounds.
    range_size = max_bound - min_bound + 1
    new_pos = (new_pos - min_bound) % range_size + min_bound

    return (new_pos, num_wraps)


def do_d1p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    parsed_data = parse_input(raw_data)
    #logging.debug("Parsed data %s:\n", {parsed_data})

    bounds = (0, 99)
    current_pos = 50
    password = 0
    for instruction in parsed_data:
        current_pos, _ = get_new_position(current_pos, instruction, bounds)
        logging.debug("New position: %d", current_pos)
        if current_pos == 0:
            logging.debug("Reached position 0!")
            password += 1
    return password


def do_d1p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    parsed_data = parse_input(raw_data)
    #logging.debug("Parsed data %s:\n", {parsed_data})

    bounds = (0, 99)
    current_pos = 50
    password = 0
    for instruction in parsed_data:
        current_pos, num_wraps = get_new_position(current_pos, instruction, bounds)
        logging.debug("New position: %d, num wraps: %s", current_pos, num_wraps)
        password += num_wraps
        if current_pos == 0:
            password += 1
    return password


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
