import csv
import math
from dataclasses import dataclass
from reprlib import recursive_repr
from typing import *
import sys
sys.setrecursionlimit(10_000)


# Put your data definitions first!
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: float|None
    electricity_and_heat_co2_emissions_per_capita: float|None
    energy_co2_emissions: float|None
    energy_co2_emissions_per_capita: float|None
    total_co2_emissions_excluding_lucf: float|None
    total_co2_emissions_excluding_lucf_per_capita: float|None

@dataclass(frozen=True)
class Node:
    value: Row
    next: Node|None

# Then your functions.
#test
# Purpose: Convert one CSV row, represented as a list of strings, into a Row object.

def parse_row(fields: list[str]) -> Row:
        new_row = Row(country = fields[0],
                      year = int(fields[1]) if fields[1] != "" else None,
                      electricity_and_heat_co2_emissions = float(fields[2]) if fields[2] != "" else None,
                      electricity_and_heat_co2_emissions_per_capita = float(fields[3]) if fields[3] != "" else None,
                      energy_co2_emissions = float(fields[4]) if fields[4] != "" else None,
                      energy_co2_emissions_per_capita = float(fields[5]) if fields[5] != "" else None,
                      total_co2_emissions_excluding_lucf = float(fields[6]) if fields[6] != "" else None,
                      total_co2_emissions_excluding_lucf_per_capita = float(fields[7]) if fields[7] != "" else None)
        return new_row

# Purpose: Recursively convert a list of Row objects into a linked list of Nodes.
def recursive_func(objs: list[Row])-> Optional[Node]:
    if objs == []:
        return None
    return Node(objs[0],recursive_func(objs[1:]))



# Purpose: Read a CSV file and return its rows as a linked list of Row nodes.
def read_csv_lines(filename: str) -> Optional[Node]:
    try:
        with open(filename, newline='') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',')
            next(all_rows)
            list_of_rows = []
            for row in all_rows:
                list_of_rows.append(parse_row(row))
            linked_list = recursive_func(list_of_rows)
            return linked_list
    except FileNotFoundError:
        return None

# Purpose: Return the number of nodes in a linked list recursively.
def listlen(data: Optional[Node]) -> int:
    if data is None:
        return 0
    return 1 + listlen(data.next)

# Purpose: Return a new linked list containing only rows that match the given filter.
def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:
    if data is None:
        return None
    if field_name == "country" and comparison != "equal":
        raise ValueError
    field_value = getattr(data.value, field_name)
    if field_value is None:
        return filter_rows(data.next, field_name, comparison, value)
    if comparison == "less_than":
        if field_value < value:
            return Node(data.value, filter_rows(data.next, field_name, comparison, value))
    elif comparison == "greater_than":
        if field_value > value:
            return Node(data.value, filter_rows(data.next, field_name, comparison, value))
    elif comparison == "equal":
        if field_value == value:
            return Node(data.value, filter_rows(data.next, field_name, comparison, value))
    return filter_rows(data.next, field_name, comparison, value)