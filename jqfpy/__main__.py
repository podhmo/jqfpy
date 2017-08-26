import sys
import json
import argparse
from jqfpy import transform


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("code")
    parser.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("-c", "--compact-output", action="store_true")
    parser.add_argument("--squash", action="store_true")
    args = parser.parse_args()
    run(
        args.input,
        args.code,
        squash=args.squash,
        compact_output=args.compact_output,
    )


def run(stream, code, *, squash=False, compact_output=False):
    opts = {"ensure_ascii": False}
    if not compact_output:
        opts["indent"] = 2

    def dump(d):
        json.dump(d, fp=sys.stdout, **opts)
        print()

    d = json.load(stream)
    r = transform(d, code)
    if squash:
        for line in r:
            dump(line)
    else:
        dump(r)


if __name__ == "__main__":
    main()
