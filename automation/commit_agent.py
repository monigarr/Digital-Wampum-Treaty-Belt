import csv
import datetime
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "belt/2025/contributions_2025.csv"
LOG_DIR = BASE_DIR / "belt/2025"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def git(cmd):
    subprocess.run(["git"] + cmd, check=True)

def today_cell():
    today = datetime.date.today()
    week = today.isocalendar()[1]
    day = today.strftime("%a")
    return week, day

def commits_for_today():
    week, day = today_cell()
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["week"]) == week:
                return int(row.get(day, 0))
    return 0

def make_commit(i):
    log = LOG_DIR / f"week_{datetime.date.today().isocalendar()[1]:02}.md"
    log.touch(exist_ok=True)
    with log.open("a") as f:
        f.write(f"{datetime.datetime.now().isoformat()} — Presence recorded ({i+1})\n")
    git(["add", str(log)])
    git(["commit", "-m", f"Witness presence {i+1}"])

def main():
    count = commits_for_today()
    for i in range(count):
        make_commit(i)

if __name__ == "__main__":
    main()
