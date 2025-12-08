#!/usr/bin/env python

import argparse
import logging
import operator
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d6p1_ex.txt" #r"data/d6p1_ex.txt"
P2_DATFILE =  P1_DATFILE #r"data/d6p1_ex.txt"

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
    d6p1 = do_d6p1(P1_DATFILE)
    logging.info(f"Part 1: {d6p1}") # 6417439773370

    # Part 2.
    d6p2 = do_d6p2(P2_DATFILE)
    logging.info(f"Part 2: {d6p2}") # 


    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_input(raw_data: list[str]) -> list[list[int|str]]:
    problems = []
    for d in raw_data:
        problems.append(d.split())
        # datalist = d.split()
        # if (datalist[0]).isnumeric():
        #     problems.append([int(x) for x in datalist])
        # else:
        #     problems.append(datalist)
    return problems


def do_d6p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    parsed_input = parse_input(raw_data)
    logging.debug("Parsed input: %s", parsed_input)

    op_key = {"+": operator.add, "*": operator.mul}
    problem_sum = 0

    for problem in zip(*parsed_input):
        op = op_key[problem[-1]]
        if op == operator.add:
            problem_res = 0
        elif op == operator.mul:
            problem_res = 1
        for val in problem[:-1]:
            problem_res = op(problem_res, int(val))
        problem_sum += problem_res
        logging.debug("Problem: %s = %d", problem, problem_res)

    return problem_sum


def do_d6p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    # Will need to parse to string and preserve the original left/right justification.
    parsed_input = parse_input(raw_data)
    logging.info("Parsed input: %s", parsed_input)

    op_key = {"+": operator.add, "*": operator.mul}
    problem_sum = 0

    transposed_problems = list(zip(*parsed_input))
    for problem in transposed_problems:
        op = op_key[problem[-1]]
        if op == operator.add:
            problem_res = 0
        elif op == operator.mul:
            problem_res = 1
        # Re-stringify the numbers.
        str_problem = [str(x) for x in problem[:-1]]
        # Pad out the strings in number format with spaces to align them.
        max_len = max(len(s) for s in str_problem)
        padded_problem = [(s[::-1]).rjust(max_len) for s in str_problem]
        new_numbers = []
        for i in range(max_len):
            this_digit = ""
            for pp in padded_problem:
                this_digit += pp[i]
            new_numbers.append(int(this_digit))
        logging.info("Problem: %s -> New numbers: %s", padded_problem, new_numbers)
        for val in new_numbers:
            problem_res = op(problem_res, val)

        problem_sum += problem_res

    return problem_sum


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
