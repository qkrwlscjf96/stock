from pathlib import Path
from datetime import datetime
import re

def already_ran_today(joblog_path: Path) -> bool:
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = re.compile(r"=== START (\d{4}-\d{2}-\d{2})")

    if not joblog_path.exists():
        return False

    with joblog_path.open("r", encoding="utf-8") as f:
        return any(
            (m := pattern.search(line)) and m.group(1) == today
            for line in f
        )