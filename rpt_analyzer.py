
import re
from pathlib import Path

input_file = Path("data/timing_report.rpt")
output_file = Path("output/rpt_timing_summary.txt")

timing_paths = []

# Read the timing report
try:
    report_text = input_file.read_text(encoding="utf-8")
except OSError as error:
    print(f"Error reading report: {error}")
    raise SystemExit(1)

# Split the report into individual timing paths
blocks = re.split(r"(?=Startpoint:)", report_text)

for block in blocks:
    startpoint_match = re.search(r"Startpoint:\s*(.+)", block)
    endpoint_match = re.search(r"Endpoint\s*:\s*(.+)", block)
    slack_match = re.search(
        r"slack\s*\((MET|VIOLATED)\)\s+(-?\d+(?:\.\d+)?)",
        block,
    )

    if startpoint_match and endpoint_match and slack_match:
        startpoint = startpoint_match.group(1).strip()
        endpoint = endpoint_match.group(1).strip()
        status = slack_match.group(1)
        slack = float(slack_match.group(2))

        timing_paths.append({
            "startpoint": startpoint,
            "endpoint": endpoint,
            "status": status,
            "slack": slack,
        })

# Calculate timing statistics
total_paths = len(timing_paths)

violating_paths = [
    path for path in timing_paths
    if path["slack"] < 0
]

passing_paths = [
    path for path in timing_paths
    if path["slack"] >= 0
]

worst_slack = min(
    (path["slack"] for path in timing_paths),
    default=None,
)

# Sort violations from worst to least severe
top_violations = sorted(
    violating_paths,
    key=lambda path: path["slack"],
)[:3]

# Build the detailed report
report_lines = [
    "===== Timing Report Summary =====",
    f"Total paths     : {total_paths}",
    f"Violating paths : {len(violating_paths)}",
    f"Passing paths   : {len(passing_paths)}",
    (
        f"Worst slack     : {worst_slack:.2f} ns"
        if worst_slack is not None
        else "Worst slack     : N/A"
    ),
    "",
    "===== Violating Paths =====",
]

if violating_paths:
    for path in sorted(violating_paths, key=lambda p: p["slack"]):
        report_lines.append(
            f'{path["startpoint"]} -> {path["endpoint"]} '
            f'| Slack: {path["slack"]:.2f} ns'
        )
else:
    report_lines.append("No timing violations found.")

# Save the detailed report
try:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )
except OSError as error:
    print(f"Error saving report: {error}")
    raise SystemExit(1)

# Print concise terminal output
print("\n===== Timing Summary =====")
print(f"Total Paths : {total_paths}")
print(f"Violations  : {len(violating_paths)}")
print(f"Passing     : {len(passing_paths)}")

if worst_slack is not None:
    print(f"Worst Slack : {worst_slack:.2f} ns")
else:
    print("Worst Slack : N/A")

print("\nTop Violations:")

if top_violations:
    for path in top_violations:
        startpoint = path["startpoint"].split()[0]
        endpoint = path["endpoint"].split()[0]

        print(
            f'{startpoint:<18} -> {endpoint:<18} '
            f'{path["slack"]:>7.2f} ns'
        )
else:
    print("No timing violations found.")

print(f"\nReport saved: {output_file}")
