import argparse
import sys

from extractor import extract, cleanup
from parser import parse
from evaluator import evaluate
from reporter import report


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a LinkedIn profile using your data export ZIP."
    )
    parser.add_argument(
        "--zip",
        required=True,
        metavar="PATH",
        help="Path to your LinkedIn data export ZIP file",
    )
    parser.add_argument(
        "--output",
        default="console",
        metavar="PATH",
        help='Output destination: "console" (default) or a file path (e.g. report.md)',
    )

    args = parser.parse_args()

    temp_dir = None
    try:
        print("Extracting ZIP...", file=sys.stderr)
        temp_dir, files = extract(args.zip)

        print("Parsing profile data...", file=sys.stderr)
        profile = parse(files)

        print("Sending to Claude for evaluation...", file=sys.stderr)
        evaluation = evaluate(profile)

        report(evaluation, profile, output=args.output)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if temp_dir:
            cleanup(temp_dir)


if __name__ == "__main__":
    main()
