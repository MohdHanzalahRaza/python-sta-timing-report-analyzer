# Python-Based STA Timing Report Analyzer

A beginner VLSI scripting project that analyzes sample Static Timing Analysis (STA) reports using Python.

## Features

- Extracts timing startpoints and endpoints from a supported plain-text timing report.
- Identifies passing paths and negative-slack violations.
- Calculates total paths, violation count, passing count, and worst slack.
- Displays a concise timing summary.
- Saves a detailed report to an output text file.
- Includes a separate CSV timing-report analyzer.

## Technologies

- Python
- Regular expressions
- CSV processing
- File handling
- Command-line scripting

## Project Structure

```text
timing-report-analyzer/
├── data/
├── output/
├── timing_analyzer.py
├── rpt_analyzer.py
├── main.py
├── README.md
└── .gitignore
```

## How to Run

Run the plain-text report analyzer:

```bash
python rpt_analyzer.py
```

Run the CSV analyzer:

```bash
python timing_analyzer.py
```

The current scripts use predefined input paths. The main command-line controller is an ongoing improvement.

## Concepts Practiced

- Timing slack
- Timing violations
- Worst slack
- Startpoints and endpoints
- Python file handling and regular expressions

## Limitations

The parser is designed for the supplied sample report format. It has not been validated against every commercial EDA timing-report format.
