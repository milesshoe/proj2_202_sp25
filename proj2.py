import csv
import math
from dataclasses import dataclass
from typing import *
import sys
sys.setrecursionlimit(10_000)


# Put your data definitions first!
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: float|None
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
# Task 2
def parse_row(fields: list[str]) -> Row:
        new_row = Row(country = fields[0],
                      year = int(fields[1] if fields[1] is not "" else 0),
                      electricity_and_heat_co2_emissions = float(fields[2] if fields[2] is not "" else 0),
                      energy_co2_emissions = float(fields[3] if fields[3] is not "" else 0),
                      energy_co2_emissions_per_capita = float(fields[4] if fields[4] is not "" else 0),
                      total_co2_emissions_excluding_lucf = float(fields[5] if fields[5] is not "" else 0),
                      total_co2_emissions_excluding_lucf_per_capita = float(fields[6] if fields[6] is not "" else 0))
        print(new_row)

def read_csv_lines(filename: str) -> Optional[Node]:
    with open(filename, newline='') as csvfile:
        all_rows = csv.reader(csvfile, delimiter=',')
        header = next(all_rows)
        for row in all_rows:
            row_class = parse_row(row)






read_csv_lines("some-ghg-emissions.csv")