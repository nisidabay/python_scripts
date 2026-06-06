#!/usr/bin/env python3
# argparse_03: type= cast, choices=, and nargs — a deploy script
import argparse

parser = argparse.ArgumentParser(description="Deploy a service to N servers with a chosen format.")
parser.add_argument("--replicas", type=int, default=1, help="Number of server instances (int)")
parser.add_argument("--cpu", type=float, default=0.5, help="CPU cores per instance (float)")
parser.add_argument("--output", choices=["json", "csv"], default="json",
                    help="Output format for the deploy manifest")
parser.add_argument("hosts", nargs="+", metavar="HOST",
                    help="One or more target hostnames/IPs")
args = parser.parse_args()

print(f"Deploying {args.replicas} replica(s) with {args.cpu} CPU to: {', '.join(args.hosts)}")
print(f"Manifest format: {args.output}")


if __name__ == "__main__":
    pass
