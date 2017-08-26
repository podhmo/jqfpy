import sys
import argparse
import jqfpy
import jqfpy.loader as loader
import jqfpy.dumper as dumper


def _describe_pycode(pycode, *, indent="", fp=sys.stderr):
    print(indent + pycode.replace("\n", "\n" + indent), file=fp)


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
    parser.add_argument("--show-code-only", action="store_true")

    args = parser.parse_args()

    rvalname = jqfpy.create_rvalname()
    pycode = jqfpy.create_pycode(args.code, rvalname)

    if args.show_code_only:
        _describe_pycode(pycode, fp=sys.stdout, indent="")
        sys.exit(0)

    d = loader.load(args.input, slurp=args.slurp_input)
    try:
        r = jqfpy.exec_pycode(d, pycode, rvalname)
    except Exception as e:
        fp = sys.stderr
        print("\x1b[32m\x1b[1mcode:\x1b[0m", file=fp)
        print("----------------------------------------", file=fp)
        print("\x1b[0m", file=fp)
        _describe_pycode(pycode, fp=fp, indent="")
        print("\x1b[0m", file=fp)
        print("----------------------------------------", file=fp)
        print("", file=fp)
        print("\x1b[32m\x1b[1merror:\x1b[0m", file=fp)
        raise

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
