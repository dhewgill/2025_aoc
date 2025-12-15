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

    def coords(self) -> tuple[int]:
        return self._coords

    def __repr__(self) -> str:
        return f"Node{self._coords}"


class Circuit:
    def __init__(self, nodes: set[Node]) -> None:
        self.nodes = nodes

    def add_nodes(self, nodes: set[Node]) -> None:
        self.nodes.update(nodes)

    def connect_circuit(self, circuit: 'Circuit') -> None:
        self.nodes.update(circuit.nodes)

    def is_connected(self, circuit: 'Circuit') -> bool:
        return any(n in self.nodes for n in circuit.nodes)

    def is_connected_node(self, node: Node) -> bool:
        return node in self.nodes

    def length(self) -> int:
        return len(self.nodes)

    def __len__(self) -> int:
        return len(self.nodes)

    def __repr__(self) -> str:
        return f"Circuit({self.nodes})"


def parse_to_nodes(raw_data: list[str]) -> list[Node]:
    nodes = []
    for line in raw_data:
        coords = tuple(int(c) for c in line.split(","))
        nodes.append(Node(coords))
    return nodes


def print_circuits(circuits: list[list[Node]]) -> None:
    for i, c in enumerate(circuits):
        logging.info("Circuit %d: %d", i, len(c))


def merge_circuits(
    circuits: list[set[tuple[int]]], new_circuit: list[set[tuple[int]]]
) -> list[set[tuple[int]]]:
    """
    Merge new circuits into existing circuits.
    If all nodes in new_circuit are already in circuits, do nothing.
    If some nodes in new_circuit are in circuits, merge those circuits.
    If no nodes in new_circuit are in circuits, add new_circuit to circuits.
    Args:
        circuits (list[set[tuple[int]]]): Existing circuits.
        new_circuit (list[set[tuple[int]]]): New circuit to merge. Usually 2-tuple.
    """
    merged = []
    for c in circuits:
        if c.intersection(new_circuit):
            for nc in new_circuit:
                c.add(nc)
    return merged


def do_d8p1(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    junction_boxes = parse_to_nodes(raw_data)
    logging.info("Parsed %d junction boxes.", len(junction_boxes))

    distances = {} # Keyed by tuple of Node pairs, value is distance.
    for box in junction_boxes:
        for other_box in junction_boxes:
            if box == other_box:
                continue
            if ((other_box, box) in distances) or ((box, other_box) in distances):
                continue
            dist = box.distance(other_box)
            distances[(box, other_box)] = dist
    logging.info("Calculated %d distances.", len(distances))
    sorted_distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    logging.debug("Sorted distances: %s", sorted_distances)

    circuits = [set((jb.coords(),)) for jb in junction_boxes]
    logging.info("Initial circuits: %s", len(circuits))
    #logging.info("Boxes: %s", tuple(sorted_distances.keys()))
    max_connections = 10
    num_connections = 0
    for boxes, dist in sorted_distances.items():
        if num_connections >= max_connections:
            break
        num_connections +=1
        box_coords = tuple(b.coords() for b in boxes)
        #logging.info("Box coords: %s", box_coords)
        for c in circuits[:]:
            for boxc in box_coords:
                if boxc in c:
                    logging.info("Removing box coord %s from circuit %s", boxc, c)
                    circuits.remove(set((boxc,)))

    logging.info("Final circuits: %s", len(circuits))
    return None


def do_d8p2(datafile: str) -> int:
    raw_data = parse_file(datafile)
    logging.debug("Raw data: %s", raw_data)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
