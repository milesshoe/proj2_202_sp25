from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)


@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: float | None
    electricity_and_heat_co2_emissions_per_capita: float | None
    energy_co2_emissions: float | None
    energy_co2_emissions_per_capita: float | None
    total_co2_emissions_excluding_lucf: float | None
    total_co2_emissions_excluding_lucf_per_capita: float | None


@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None


EXPECTED_HEADER = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita",
]


# Purpose: Convert an empty string to None, otherwise convert the string to a float.
def parse_float(value: str) -> float | None:
    if value == "":
        return None
    return float(value)


# Purpose: Convert one CSV row, represented as a list of strings, into a Row object.
def parse_row(fields: list[str]) -> Row:
    return Row(
        country=fields[0],
        year=int(fields[1]),
        electricity_and_heat_co2_emissions=parse_float(fields[2]),
        electricity_and_heat_co2_emissions_per_capita=parse_float(fields[3]),
        energy_co2_emissions=parse_float(fields[4]),
        energy_co2_emissions_per_capita=parse_float(fields[5]),
        total_co2_emissions_excluding_lucf=parse_float(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita=parse_float(fields[7]),
    )


# Purpose: Recursively convert a list of Row objects into a linked list of Nodes.
def recursive_func(objs: list[Row]) -> Optional[Node]:
    if objs == []:
        return None
    return Node(objs[0], recursive_func(objs[1:]))


# Purpose: Read a CSV file and return its rows as a linked list of Row nodes.
def read_csv_lines(filename: str) -> Optional[Node]:
    try:
        with open(filename, newline="") as csvfile:
            all_rows = csv.reader(csvfile, delimiter=",")

            header = next(all_rows)
            if header != EXPECTED_HEADER:
                raise ValueError("unexpected header")

            list_of_rows = []
            for row in all_rows:
                if row != []:
                    list_of_rows.append(parse_row(row))

            return recursive_func(list_of_rows)

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
    value: Union[str, float, int],
) -> Optional[Node]:
    if data is None:
        return None

    if field_name == "country" and comparison != "equal":
        raise ValueError

    field_value = getattr(data.value, field_name)

    if field_value is None:
        return filter_rows(data.next, field_name, comparison, value)

    rest = filter_rows(data.next, field_name, comparison, value)

    if comparison == "less_than":
        if field_value < value:
            return Node(data.value, rest)
    elif comparison == "greater_than":
        if field_value > value:
            return Node(data.value, rest)
    elif comparison == "equal":
        if field_value == value:
            return Node(data.value, rest)
    else:
        raise ValueError

    return rest