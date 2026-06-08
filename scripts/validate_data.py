#!/usr/bin/env python3
"""Validate kaoyan research records in CSV or JSON format."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


IDENTITY_FIELDS = ("year", "school", "college", "major_code", "major_name", "study_mode")
NUMERIC_FIELDS = (
    "national_line",
    "retest_line",
    "planned_total",
    "recommended_exempt",
    "unified_quota",
    "applicants",
    "retest_count",
    "admitted_count",
    "admitted_min",
    "admitted_median",
    "admitted_mean",
)
ANALYSIS_FIELDS = NUMERIC_FIELDS + ("subject_change",)


def load_records(path: Path) -> list[dict[str, object]]:
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("JSON must be an array of objects")
        return data
    raise ValueError("Only .csv and .json files are supported")


def is_blank(value: object) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate(records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    seen: set[tuple[str, ...]] = set()

    if not records:
        return ["No records found"]

    for index, row in enumerate(records, start=2):
        if is_blank(row.get("year")):
            errors.append(f"row {index}: missing year")
        if is_blank(row.get("school")):
            errors.append(f"row {index}: missing school")
        if is_blank(row.get("college")):
            errors.append(f"row {index}: missing college")
        if is_blank(row.get("major_code")) and is_blank(row.get("major_name")):
            errors.append(f"row {index}: provide major_code or major_name")
        if is_blank(row.get("study_mode")):
            errors.append(f"row {index}: missing study_mode")
        if not any(not is_blank(row.get(field)) for field in ANALYSIS_FIELDS):
            errors.append(f"row {index}: no analyzable fields")

        for field in NUMERIC_FIELDS:
            value = row.get(field)
            if is_blank(value):
                continue
            try:
                number = float(str(value))
                if number < 0:
                    errors.append(f"row {index}: {field} cannot be negative")
            except ValueError:
                errors.append(f"row {index}: {field} must be numeric")

        key = tuple(str(row.get(field, "")).strip() for field in IDENTITY_FIELDS)
        if key in seen:
            errors.append(f"row {index}: duplicate research object and year")
        seen.add(key)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_data.py DATA.csv|DATA.json", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        records = load_records(path)
        errors = validate(records)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    print(f"OK: {len(records)} record(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

