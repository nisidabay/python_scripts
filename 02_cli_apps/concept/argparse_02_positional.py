#!/usr/bin/env python3
# argparse_02: Required positional args, help text, metavar — a file converter
import argparse

parser = argparse.ArgumentParser(description="Convert a media file from one format to another.")
parser.add_argument("input_file", metavar="INPUT", help="Path to the source file")
parser.add_argument("output_file", metavar="OUTPUT", help="Path for the converted file")
args = parser.parse_args()

print(f"Converting {args.input_file} → {args.output_file}")
# In a real app: detect format, run ffmpeg/magick, write output


if __name__ == "__main__":
    pass
