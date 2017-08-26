import sys
import argparse
from jqfpy import transform
import jqfpy.loader as loader
import jqfpy.dumper as dumper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("code", nargs="?", default="get()")
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("-c", "--compact-output", action="store_true")
    parser.add_argument("-s", "--slurp-input", action="store_true")
    parser.add_argument("-S", "--sort-keys", action="store_true")
    parser.add_argument("-a", "--ascii-output", action="store_true")
    parser.add_argument("-r", "--raw-output", action="store_true")
    parser.add_argument("--squash", action="store_true")

    args = parser.parse_args()

    d = loader.load(args.input, slurp=args.slurp_input)
    r = transform(d, args.code)
    dumper.dump(
        r,
        fp=sys.stdout,
        squash=args.squash,
        compact=args.compact_output,
        raw=args.raw_output,
        json_kwargs=dict(
            sort_keys=args.sort_keys,
            ensure_ascii=args.ascii_output,
        ),
    )


if __name__ == "__main__":
    main()
