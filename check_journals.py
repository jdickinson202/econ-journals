"""Check journals.csv: its format, and that each OpenAlex ID still points at the journal with that ISSN.

Needs only Python. Run it with: python check_journals.py
"""

import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

COLUMNS = ["openalex_id", "journal", "jel", "field", "rank", "issn", "repec"]
OPENALEX = "https://api.openalex.org/sources"
USER_AGENT = "econ-journals check (https://github.com/jdickinson202/econ-journals)"
PATTERNS = {
    "openalex_id": r"S\d+",
    "jel": r"TOP|[A-RYZ]",
    "rank": r"[1-9]\d*",
    "issn": r"\d{4}-\d{3}[\dX]",
    "repec": r"[a-z0-9]{3}:[a-z0-9]+",
}


def format_problems(rows):
    problems = []
    for number, row in enumerate(rows, start=2):
        for column in COLUMNS:
            if not row[column].strip():
                if column != "repec":  # A journal may not be in RePEc.
                    problems.append(f"line {number}: {column} is empty")
            elif column in PATTERNS and not re.fullmatch(PATTERNS[column], row[column]):
                problems.append(f"line {number}: {column} is {row[column]!r}")
    for column in ("openalex_id", "journal", "issn", "repec"):
        values = [row[column] for row in rows if row[column]]
        for value in sorted({value for value in values if values.count(value) > 1}):
            problems.append(f"{value} is listed twice under {column}")
    for jel in sorted({row["jel"] for row in rows}):
        group = [row for row in rows if row["jel"] == jel]
        if len({row["field"] for row in group}) > 1:
            problems.append(f"{jel} has more than one field name")
        if sorted(row["rank"] for row in group) != sorted(str(n + 1) for n in range(len(group))):
            problems.append(f"{jel}'s ranks should run from 1 to {len(group)}")
    return problems


def ask_openalex(ids):
    query = urllib.parse.urlencode(
        {"filter": "openalex:" + "|".join(ids), "per-page": len(ids), "select": "id,display_name,issn_l"}, safe=":|")
    request = urllib.request.Request(f"{OPENALEX}?{query}", headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)["results"]
        except urllib.error.URLError:  # OpenAlex having a bad moment says nothing about the list.
            if attempt == 2:
                raise
            time.sleep(20)


def openalex_problems(rows):
    problems = []
    for start in range(0, len(rows), 50):
        chunk = rows[start:start + 50]
        found = {source["id"].rsplit("/", 1)[-1]: source for source in ask_openalex([row["openalex_id"] for row in chunk])}
        for row in chunk:
            source = found.get(row["openalex_id"])
            if source is None:
                problems.append(f"{row['journal']}: OpenAlex has no {row['openalex_id']}")
            elif source["issn_l"] != row["issn"]:
                problems.append(f"{row['journal']}: {row['openalex_id']} is now {source['display_name']!r}, "
                                f"ISSN {source['issn_l']}, not {row['issn']}")
    return problems


def main():
    with open("journals.csv", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != COLUMNS:
            sys.exit(f"The columns should be {COLUMNS}, not {reader.fieldnames}")
        rows = list(reader)
    problems = format_problems(rows)
    if not problems:  # A list in the wrong shape would only confuse the next step.
        problems = openalex_problems(rows)
    for problem in problems:
        print(problem)
    if problems:
        sys.exit(f"{len(problems)} problems in journals.csv")
    print(f"journals.csv is fine: {len(rows)} journals, and OpenAlex agrees on each.")


if __name__ == "__main__":
    main()
