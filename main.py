
import argparse
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PARSERS = {
    ".csv": "timing_analyzer.py",
    ".rpt": "rpt_analyzer.py",
}


def main():
    parser = argparse.ArgumentParser(
        description="Analyze CSV or plain-text STA timing reports."
    )

    parser.add_argument(
        "report",
        help="Path to a timing report (.csv or .rpt)",
    )

    args = parser.parse_args()
    report_path = Path(args.report)

    if not report_path.is_absolute():
        report_path = BASE_DIR / report_path

    if not report_path.is_file():
        parser.error(f"Report file not found: {report_path}")

    extension = report_path.suffix.lower()

    if extension not in PARSERS:
        parser.error("Supported formats: .csv and .rpt")

    script_path = BASE_DIR / PARSERS[extension]

    if not script_path.is_file():
        parser.error(f"Analyzer script not found: {script_path}")

    print(f"Analyzing: {report_path.name}")
    print(f"Format: {extension[1:].upper()}\n")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
