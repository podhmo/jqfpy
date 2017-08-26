import argparse
import sys
from jqfpy import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("code")
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("--squash", action="store_true")
    args = parser.parse_args()
    run(args.input, args.code, squash=args.squash)


if __name__ == "__main__":
    main()
