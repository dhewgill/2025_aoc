#!/usr/bin/env python

import argparse
import logging
import operator
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r"data/d6p1.txt" #r"data/d6p1_ex.txt"
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
def parse_input(raw_data: list[str], split_line:bool=True) -> list[list[int|str]]:
    problems = []
    for d in raw_data:
        if split_line:
            problems.append(d.split())
        else:
            problems.append(d)
    return problems


def split_to_problems(probs: list[str]) -> list[list[str]]:
    problem_list = []

    max_cols = len(probs[0])
    prob_start_index = 0
    for col in range(max_cols):
        if all(p[col] == " " for p in probs):
            # We've reached the end of a problem.
            problem_list.append(tuple(p[prob_start_index:col] for p in probs))
            prob_start_index = col + 1

    # Add the last problem.
    problem_list.append(tuple(p[prob_start_index:] for p in probs))
    return problem_list


def compute_problem_value(problem: list[str], op_func) -> int:
    if op_func == operator.add:
        problem_res = 0
    elif op_func == operator.mul:
        problem_res = 1

    max_cols = len(problem[0])
    for col in range(max_cols-1, -1, -1): # Count backwards; right to left.
        this_val = ""
        vals = []
        for p in problem: # Iterate by rows of the problem.
            if p[col] != " ":
                this_val += p[col]
        val = int(this_val)
        vals.append(val)
        logging.debug("Column %d: Values: %s", col, vals)
        problem_res = op_func(problem_res, val)

    return problem_res


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
    parsed_input = parse_input(raw_data, False)
    logging.debug("Parsed input: %s", parsed_input)

    op_key = {"+": operator.add, "*": operator.mul}
    op_line = parsed_input.pop()
    ops = op_line.split()
    logging.debug("Operators: %s", ops)
    problem_sum = 0

    probs = split_to_problems(parsed_input)
    logging.debug("Problems: %s", probs)

    for problem, op in zip(probs, ops):
        problem_res = compute_problem_value(problem, op_key[op])
        problem_sum += problem_res
        logging.debug("Problem: %s = %d", problem, problem_res)

    return problem_sum


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
