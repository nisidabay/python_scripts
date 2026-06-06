#!/usr/bin/env python3
# argparse_05: Mutually exclusive group — a notification sender
import argparse

parser = argparse.ArgumentParser(description="Send a notification via one of several channels.")

# Exactly one transport must be chosen
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--email", metavar="ADDR", help="Send via email to ADDR")
group.add_argument("--sms", metavar="PHONE", help="Send via SMS to PHONE")
group.add_argument("--slack", metavar="CHANNEL", help="Send to Slack #CHANNEL")
group.add_argument("--push", action="store_true", help="Send as push notification")

parser.add_argument("message", help="Notification body text")
args = parser.parse_args()

if args.email:
    print(f"Sending email to {args.email}: {args.message}")
elif args.sms:
    print(f"Sending SMS to {args.sms}: {args.message}")
elif args.slack:
    print(f"Sending Slack message to {args.slack}: {args.message}")
elif args.push:
    print(f"Sending push notification: {args.message}")


if __name__ == "__main__":
    pass
