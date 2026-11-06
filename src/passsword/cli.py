import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Passsword",
        description="Password tool",
        epilog="Thank you for using Passsword"
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Sub-commands"
    )

    generate = subparsers.add_parser(
        "generate",
        help="Generate password"
    )

    subparsers.add_parser(
        "check",
        help="Check password"
    )

    subparsers.add_parser(
        "leaked",
        help="If your password is leaked on internet"
    )

    args = parser.parse_args()

    print(f"The chosen subcommand is: {args.command}")
    if args.command == "generate":
        print("generate")
    elif args.command == "check":
        print("check")
    elif args.command == "leaked":
        print("leaked")
