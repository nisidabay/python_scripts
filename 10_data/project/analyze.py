#!/usr/bin/env python3
"""CSV data analyzer — load, filter, groupby, pivot, export. Uses pandas + numpy."""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error reading {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def parse_filter(filter_str: str) -> tuple[str, float | str, str]:
    """Parse a simple filter expression like 'col>5' or 'col==foo'.

    Supports: >, <, >=, <=, ==, !=
    """

    # Try each operator
    for op in (">=", "<=", "!=", "==", ">", "<"):
        if op in filter_str:
            col, val = filter_str.split(op, 1)
            col, val = col.strip(), val.strip()
            # Try numeric conversion
            try:
                val_num = float(val)
                if op == ">":
                    return col, val_num, "gt"
                elif op == "<":
                    return col, val_num, "lt"
                elif op == ">=":
                    return col, val_num, "ge"
                elif op == "<=":
                    return col, val_num, "le"
                elif op == "==":
                    if val_num == int(val_num):
                        val_num = int(val_num)
                    return col, val_num, "eq"
                elif op == "!=":
                    return col, val_num, "ne"
            except ValueError:
                # String value
                if op == "==":
                    return col, val, "eq"
                elif op == "!=":
                    return col, val, "ne"
                else:
                    print(f"Error: cannot compare string with '{op}'", file=sys.stderr)
                    sys.exit(1)

    print(f"Error: could not parse filter '{filter_str}'", file=sys.stderr)
    sys.exit(1)


def apply_filters(df: pd.DataFrame, filters: list[str]) -> pd.DataFrame:
    """Apply a list of filter strings to the DataFrame."""
    for f in filters:
        col, val, op = parse_filter(f)
        if col not in df.columns:
            print(f"Error: column '{col}' not found", file=sys.stderr)
            sys.exit(1)

        if op == "gt":
            df = df[df[col] > val]
        elif op == "lt":
            df = df[df[col] < val]
        elif op == "ge":
            df = df[df[col] >= val]
        elif op == "le":
            df = df[df[col] <= val]
        elif op == "eq":
            df = df[df[col] == val]
        elif op == "ne":
            df = df[df[col] != val]

    return df


def cmd_summary(args) -> int:
    df = load_csv(args.input)
    print(f"File: {args.input}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
    print("Column info:")
    print(df.dtypes.to_string())
    print(f"\nMissing values:\n{df.isnull().sum().to_string()}")
    print(f"\nBasic stats:\n{df.describe(include='all').to_string()}")
    return 0


def cmd_groupby(args) -> int:
    df = load_csv(args.input)

    if args.filter:
        df = apply_filters(df, args.filter)

    if args.groupby not in df.columns:
        print(f"Error: groupby column '{args.groupby}' not found", file=sys.stderr)
        return 1

    agg_cols = args.agg_cols or [c for c in df.columns if c != args.groupby and np.issubdtype(df[c].dtype, np.number)]
    if not agg_cols:
        print("Error: no numeric columns found for aggregation", file=sys.stderr)
        return 1

    aggs = {}
    for col in agg_cols:
        aggs[col] = args.agg_funcs

    result = df.groupby(args.groupby).agg(aggs)

    if args.sort:
        first_col = result.columns[0] if isinstance(result.columns, pd.MultiIndex) else result.columns[0]
        result = result.sort_values(first_col, ascending=args.sort_asc)

    if args.output:
        result.to_csv(args.output)
        print(f"Written to {args.output}")
    else:
        print(result.to_string())

    return 0


def cmd_pivot(args) -> int:
    df = load_csv(args.input)

    if args.filter:
        df = apply_filters(df, args.filter)

    required = [args.index, args.columns, args.values]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"Error: columns not found: {missing}", file=sys.stderr)
        return 1

    pivot = df.pivot_table(
        index=args.index,
        columns=args.columns,
        values=args.values,
        aggfunc=args.aggfunc,
        fill_value=0,
    )

    if args.output:
        pivot.to_csv(args.output)
        print(f"Written to {args.output}")
    else:
        print(pivot.to_string())

    return 0


def cmd_export(args) -> int:
    df = load_csv(args.input)

    if args.filter:
        df = apply_filters(df, args.filter)

    if args.columns:
        avail = [c for c in args.columns if c in df.columns]
        missing = set(args.columns) - set(avail)
        if missing:
            print(f"Warning: columns not found: {missing}", file=sys.stderr)
        df = df[avail]

    fmt = Path(args.output).suffix.lower()
    if fmt == ".csv":
        df.to_csv(args.output, index=False)
    elif fmt in (".xlsx", ".xls"):
        df.to_excel(args.output, index=False)
    elif fmt == ".json":
        df.to_json(args.output, orient="records", indent=2)
    elif fmt == ".parquet":
        df.to_parquet(args.output, index=False)
    else:
        print(f"Error: unsupported format '{fmt}'", file=sys.stderr)
        return 1

    print(f"Exported {df.shape[0]} rows x {df.shape[1]} columns to {args.output}")
    return 0


def cmd_head(args) -> int:
    df = load_csv(args.input)
    print(df.head(args.n).to_string())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CSV data analyzer — load, filter, groupby, pivot, export.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # summary
    p_sum = sub.add_parser("summary", help="Show summary statistics")
    p_sum.add_argument("input", help="CSV file path")

    # groupby
    p_gb = sub.add_parser("groupby", help="Group by column and aggregate")
    p_gb.add_argument("--input", required=True, help="CSV file path")
    p_gb.add_argument("--groupby", required=True, help="Column to group by")
    p_gb.add_argument("--agg", "--agg-funcs", dest="agg_funcs", nargs="+",
                       default=["mean", "sum", "count"],
                       help="Aggregation functions (default: mean sum count)")
    p_gb.add_argument("--agg-cols", nargs="+",
                       help="Columns to aggregate (default: all numeric except groupby)")
    p_gb.add_argument("--filter", action="append", default=[],
                       help="Filter expression e.g. 'age>30' (repeatable)")
    p_gb.add_argument("--sort", action="store_true", help="Sort results")
    p_gb.add_argument("--sort-asc", action="store_true", help="Sort ascending (default: descending)")
    p_gb.add_argument("--output", help="Output CSV path")

    # pivot
    p_pv = sub.add_parser("pivot", help="Create pivot table")
    p_pv.add_argument("--input", required=True, help="CSV file path")
    p_pv.add_argument("--index", required=True, help="Index column")
    p_pv.add_argument("--columns", required=True, help="Columns to pivot on")
    p_pv.add_argument("--values", required=True, help="Values column")
    p_pv.add_argument("--aggfunc", default="mean", help="Aggregation function (default: mean)")
    p_pv.add_argument("--filter", action="append", default=[],
                       help="Filter expression e.g. 'age>30' (repeatable)")
    p_pv.add_argument("--output", help="Output CSV path")

    # export
    p_exp = sub.add_parser("export", help="Export to CSV/Excel/JSON/Parquet")
    p_exp.add_argument("--input", required=True, help="CSV file path")
    p_exp.add_argument("--output", required=True, help="Output file path (csv/xlsx/json/parquet)")
    p_exp.add_argument("--columns", nargs="+", help="Columns to include (default: all)")
    p_exp.add_argument("--filter", action="append", default=[],
                       help="Filter expression e.g. 'age>30' (repeatable)")

    # head
    p_hd = sub.add_parser("head", help="Show first N rows")
    p_hd.add_argument("input", help="CSV file path")
    p_hd.add_argument("-n", type=int, default=10, help="Number of rows (default: 10)")

    args = parser.parse_args()

    if args.command == "summary":
        return cmd_summary(args)
    elif args.command == "groupby":
        return cmd_groupby(args)
    elif args.command == "pivot":
        return cmd_pivot(args)
    elif args.command == "export":
        return cmd_export(args)
    elif args.command == "head":
        return cmd_head(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
