import sys
import argparse
from jqfpy import transform
import jqfpy.loader as loader
import jqfpy.dumper as dumper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("code")
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("-c", "--compact-output", action="store_true")
    parser.add_argument("-s", "--slurp-input", action="store_true")
    parser.add_argument("--squash", action="store_true")

    args = parser.parse_args()

    run(
        args.input,
        args.code,
        squash=args.squash,
        slurp_input=args.slurp_input,
        compact_output=args.compact_output,
    )


def run(stream, code, *, squash=False, slurp_input=False, compact_output=False):
    d = loader.load(stream, slurp=slurp_input)
    r = transform(d, code)
    dumper.dump(r, fp=sys.stdout, squash=squash, compact=compact_output)


if __name__ == "__main__":
    main()
