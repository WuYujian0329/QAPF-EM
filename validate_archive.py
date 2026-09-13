"""Validate the structure and basic numeric integrity of the archived results."""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
METHODS = {"CEM", "DAEM", "SEM", "SAEM", "QAPF-EM"}
NUMERIC_SUFFIXES = ("_mean", "_sd")


def read_rows(name: str) -> list[dict[str, str]]:
    path = ROOT / "data" / name
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"{name} is empty")
    if any(not value.strip() for row in rows for value in row.values()):
        raise ValueError(f"{name} contains an empty field")
    for row_number, row in enumerate(rows, start=2):
        for field, value in row.items():
            if field.endswith(NUMERIC_SUFFIXES):
                number = float(value)
                if not math.isfinite(number):
                    raise ValueError(f"{name}:{row_number} has non-finite {field}")
                if field.endswith("_sd") and number < 0:
                    raise ValueError(f"{name}:{row_number} has negative {field}")
    return rows


def validate_simulation(rows: list[dict[str, str]]) -> None:
    if len(rows) != 45:
        raise ValueError(f"expected 45 simulation rows, found {len(rows)}")
    keys = {
        (int(row["dimension"]), int(row["model"]), int(row["components"]), row["method"])
        for row in rows
    }
    expected = {
        (dimension, model, components, method)
        for dimension in (1, 2, 3)
        for model, components in ((1, 2), (2, 4), (3, 6))
        for method in METHODS
    }
    if keys != expected:
        raise ValueError("simulation method-setting coverage is incomplete or duplicated")


def validate_real_data(rows: list[dict[str, str]]) -> None:
    if len(rows) != 15:
        raise ValueError(f"expected 15 real-data rows, found {len(rows)}")
    keys = {(row["data"], row["method"]) for row in rows}
    expected = {(dataset, method) for dataset in ("Iris", "Wine", "Seeds") for method in METHODS}
    if keys != expected:
        raise ValueError("real-data method-dataset coverage is incomplete or duplicated")


def main() -> None:
    validate_simulation(read_rows("simulation_results.csv"))
    validate_real_data(read_rows("real_data_results.csv"))
    print("Archive validation passed: 45 simulation rows and 15 real-data rows.")


if __name__ == "__main__":
    main()
