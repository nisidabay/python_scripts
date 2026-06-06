#!/usr/bin/env python3
# argparse_07: Custom type function, custom Action class, argparse.error() — a config validator
import argparse
import os


# --- Custom type: raises argparse.ArgumentTypeError on invalid input ---
def port_number(value):
    """Validate that value is an integer between 1 and 65535."""
    try:
        p = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"port must be an integer, got '{value}'")
    if not (1 <= p <= 65535):
        raise argparse.ArgumentTypeError(f"port must be 1–65535, got {p}")
    return p


def existing_file(value):
    """Ensure the file path exists."""
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError(f"file not found: {value}")
    return value


# --- Custom Action: does something at parse time beyond storing a value ---
class EnvVarAction(argparse.Action):
    """Store the argument but also export it as an environment variable."""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        os.environ[self.dest.upper()] = str(values)


parser = argparse.ArgumentParser(description="Validate and load a service configuration.")
parser.add_argument("--port", type=port_number, required=True, help="TCP port to bind (1–65535)")
parser.add_argument("--config", type=existing_file, help="Path to a JSON/YAML config file")
parser.add_argument("--env", action=EnvVarAction, default="production",
                    help="Deployment environment (stored in $ENV)")

args = parser.parse_args()

print(f"Binding to port {args.port}")
if args.config:
    print(f"Loading config from: {args.config}")
print(f"$ENV = {os.environ.get('ENV', 'not set')}")

# argparse.error() for post-parse validation
if args.port == 80 and os.geteuid() != 0:
    parser.error("Port 80 requires root privileges — run with sudo or choose a port >= 1024")


if __name__ == "__main__":
    pass
