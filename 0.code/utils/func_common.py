from pathlib import Path
from datetime import datetime
import re

def already_ran_today_twice(joblog_path: Path) -> bool:
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = re.compile(r"=== START (\d{4}-\d{2}-\d{2})")

    if not joblog_path.exists():
        return False

    with joblog_path.open("r", encoding="cp949", errors="ignore") as f:
        count = sum(
            1
            for line in f
            if (m := pattern.search(line)) and m.group(1) == today
        )

    return count >= 2