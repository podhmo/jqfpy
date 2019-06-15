import os
import sys
import contextlib
import argparse
import magicalimport

from . import loading
from . import create_pycode, exec_pycode, transform, create_context


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
    parser.add_argument(
        "-i", "--input-format", choices=["json", "yaml", "ltsv", "raw"], default="json"
    )
    parser.add_argument(
        "-o", "--output-format", choices=["json", "yaml", "ltsv", "raw"], default="json"
    )

    parser.add_argument("-c", "--compact-output", action="store_true")
    parser.add_argument("-s", "--slurp", action="store_true")
    parser.add_argument("-S", "--sort-keys", action="store_true")
    parser.add_argument("--ascii-output", action="store_true")
    parser.add_argument("-r", "--raw-output", action="store_true")
    parser.add_argument(
        "--relative-path",
        action="store_true",
        help="when h.dumpfile(), iff accessing opend filename, treating as relative path",
    )
    parser.add_argument("--here", default=None, help="cwd for h.dumpfile()")

    parser.add_argument("--buffered", action="store_true", dest="buffered")
    parser.add_argument("-u", "--unbuffered", action="store_false", dest="buffered")
    parser.set_defaults(buffered=True)

    parser.add_argument("--squash", action="count", default=0)
    parser.add_argument("--show-code", action="store_true")
    parser.add_argument("--show-none", dest="ignore_none", action="store_false")
    parser.add_argument("-a", "--additionals")

    args = parser.parse_args()

    fnname = "_transform"
    if not args.file and os.path.exists(args.code):
        args.file.append(open(args.code))
        args.code = "get()"

    pycode = create_pycode(fnname, args.code)
    fp = sys.stdout

    if args.show_code:
        _describe_pycode(pycode, fp=fp, indent="")
        sys.exit(0)

    if args.file:
        files = args.file[:]
    else:
        files = [sys.stdin]

    additionals = None
    if args.additionals is not None:
        additionals = magicalimport.import_module(args.additionals)

    dump_extra_kwargs = dict(
        indent=None if args.compact_output else 2,
        sort_keys=args.sort_keys,
        ensure_ascii=args.ascii_output,
    )
    # xxx: chdir if here is not None
    ctx = create_context(here=args.here, extra_kwargs=dump_extra_kwargs)

    with gentle_error_reporting(pycode, fp):
        transform_fn = exec_pycode(fnname, pycode)

    def _load(streams, *, relative=args.relative_path):
        for stream in streams:
            if relative:
                filepath = loading.get_filepath_from_stream(stream)
                if filepath:
                    ctx.chdir(os.path.dirname(filepath))

            m = ctx.get_module(stream, format=args.input_format)
            for d in m.load(stream, buffered=args.buffered):
                yield d

    def _dump(d, *, i=0, fp=fp, raw=False):
        m = ctx.get_module(fp, format=args.output_format)
        if i > 0 and m.SEPARATOR:
            fp.write(m.SEPARATOR)
        m.dump(
            d,
            fp=fp,
            ignore_none=args.ignore_none,
            squash_level=args.squash,
            raw=raw or args.raw_output,
            extra_kwargs=ctx.dump_extra_kwargs,
        )
        if not args.buffered:
            fp.flush()

    if args.slurp:
        d = list(_load(files))
        with gentle_error_reporting(pycode, fp):
            r = transform(ctx, transform_fn, d, additionals=additionals)
        _dump(r, i=0)
    else:
        with gentle_error_reporting(pycode, fp):
            for i, d in enumerate(_load(files)):
                r = transform(ctx, transform_fn, d, additionals=additionals)
                _dump(r, i=i)
    fp.flush()
