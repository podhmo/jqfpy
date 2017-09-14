import os
import sys
import contextlib
import argparse
import jqfpy
from jqfpy import loading


def _describe_pycode(pycode, *, indent="", fp=sys.stderr):
    print(indent + pycode.replace("\n", "\n" + indent), file=fp)


@contextlib.contextmanager
def gentle_error_reporting(pycode, fp):
    try:
        yield
    except Exception as e:
        fp = sys.stderr
        print("\x1b[32m\x1b[1mcode:\x1b[0m", file=fp)
        print("----------------------------------------", file=fp)
        _describe_pycode(pycode, fp=fp, indent="")
        print("----------------------------------------", file=fp)
        print("", file=fp)
        print("\x1b[32m\x1b[1merror:\x1b[0m", file=fp)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("code", nargs="?", default="get()")
    parser.add_argument("file", nargs="*", type=argparse.FileType("r"))
    parser.add_argument("-i", "--input-format", choices=["json", "yaml", "ltsv"], default="json")
    parser.add_argument("-o", "--output-format", choices=["json", "yaml", "ltsv"], default="json")

    parser.add_argument("-c", "--compact-output", action="store_true")
    parser.add_argument("-s", "--slurp", action="store_true")
    parser.add_argument("-S", "--sort-keys", action="store_true")
    parser.add_argument("-a", "--ascii-output", action="store_true")
    parser.add_argument("-r", "--raw-output", action="store_true")

    parser.add_argument("--buffered", action="store_true", dest="buffered")
    parser.add_argument("--unbuffered", action="store_false", dest="buffered")
    parser.set_defaults(buffered=True)

    parser.add_argument("--squash", action="store_true")
    parser.add_argument("--show-code", action="store_true")

    args = parser.parse_args()

    fnname = "_transform"
    if not args.file and os.path.exists(args.code):
        args.file.append(open(args.code))
        args.code = "get()"

    pycode = jqfpy.create_pycode(fnname, args.code)
    fp = sys.stdout

    if args.show_code:
        _describe_pycode(pycode, fp=fp, indent="")
        sys.exit(0)

    if args.file:
        files = args.file[:]
    else:
        files = [sys.stdin]

    with gentle_error_reporting(pycode, fp):
        transform_fn = jqfpy.exec_pycode(fnname, pycode)

    def _load(streams):
        for stream in streams:
            m = loading.get_module(stream, default_format=args.input_format)
            for d in m.load(stream, buffered=args.buffered):
                yield d

    def _dump(d, *, i):
        m = loading.get_module(fp, default_format=args.output_format)
        if i > 0 and m.SEPARATOR:
            fp.write(m.SEPARATOR)
        m.dump(
            d,
            fp=fp,
            squash=args.squash,
            raw=args.raw_output,
            extra_kwargs=dict(
                indent=None if args.compact_output else 2,
                sort_keys=args.sort_keys,
                ensure_ascii=args.ascii_output,
            ),
        )
        if not args.buffered:
            fp.flush()

    if args.slurp:
        d = list(_load(files))
        with gentle_error_reporting(pycode, fp):
            r = jqfpy.transform(transform_fn, d)
        _dump(r, i=0)
    else:
        with gentle_error_reporting(pycode, fp):
            for i, d in enumerate(_load(files)):
                r = jqfpy.transform(transform_fn, d)
                _dump(r, i=i)
    fp.flush()


if __name__ == "__main__":
    main()
