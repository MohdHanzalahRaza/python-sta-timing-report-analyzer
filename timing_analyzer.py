
import csv
from pathlib import Path

input_file = Path("data/timing_report.csv")
output_file = Path("output/timing_summary.txt")

total_paths = 0
violations = 0
passing_paths = 0
worst_slack = None
violating_paths = []

try:
    with input_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {"path_name", "slack_ns"}

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain path_name and slack_ns columns."
            )

        for line_number, row in enumerate(reader, start=2):
            path_name = (row.get("path_name") or "").strip()
            slack_text = (row.get("slack_ns") or "").strip()

            try:
                slack = float(slack_text)
            except ValueError:
                print(f"Warning: Invalid slack at line {line_number}. Skipping.")
                continue

            if not path_name:
                print(f"Warning: Missing path name at line {line_number}. Skipping.")
                continue

            total_paths += 1

            if slack < 0:
                violations += 1
                violating_paths.append((path_name, slack))
            else:
                passing_paths += 1

            if worst_slack is None or slack < worst_slack:
                worst_slack = slack

except (FileNotFoundError, ValueError) as error:
    print(f"Error: {error}")

else:
    report_lines = [
        "===== Timing Report Summary =====",
        f"Total valid paths : {total_paths}",
        f"Violating paths   : {violations}",
        f"Passing paths     : {passing_paths}",
        f"Worst slack       : {worst_slack:.2f} ns"
        if worst_slack is not None
        else "Worst slack       : N/A",
        "",
        "===== Violating Paths =====",
    ]

    if violating_paths:
        for path_name, slack in violating_paths:
            report_lines.append(f"{path_name:<12} {slack:>8.2f} ns")
    else:
        report_lines.append("No timing violations found.")

    report_text = "\n".join(report_lines) + "\n"

    print(report_text)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report_text, encoding="utf-8")

    print(f"Report saved to: {output_file}")
