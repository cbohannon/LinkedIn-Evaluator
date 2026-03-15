import argparse
import sys

from extractor import extract, cleanup
from parser import parse
from evaluator import evaluate, evaluate_raw
from html_parser import parse_html
from browser import fetch_profile
from reporter import report


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a LinkedIn profile using your data export ZIP, saved HTML file, or profile URL."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--zip",
        metavar="PATH",
        help="Path to your LinkedIn data export ZIP file",
    )
    input_group.add_argument(
        "--html",
        metavar="PATH",
        help="Path to a saved LinkedIn profile HTML file",
    )
    input_group.add_argument(
        "--url",
        metavar="URL",
        help="LinkedIn profile URL to fetch and evaluate using browser automation",
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
        if args.zip:
            print("Extracting ZIP...", file=sys.stderr)
            temp_dir, files = extract(args.zip)

            print("Parsing profile data...", file=sys.stderr)
            profile = parse(files)

            print("Sending to Claude for evaluation...", file=sys.stderr)
            evaluation = evaluate(profile)

            report(evaluation, profile, output=args.output)

        elif args.html:
            print("Parsing HTML...", file=sys.stderr)
            text = parse_html(args.html)

            print("Sending to Claude for evaluation...", file=sys.stderr)
            evaluation = evaluate_raw(text)

            report(evaluation, {}, output=args.output)

        elif args.url:
            print("Launching browser...", file=sys.stderr)
            text = fetch_profile(args.url)

            print("Sending to Claude for evaluation...", file=sys.stderr)
            evaluation = evaluate_raw(text)

            report(evaluation, {}, output=args.output)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
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
