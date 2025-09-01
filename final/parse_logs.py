import os
import re
import time
from datetime import datetime, timedelta
import psycopg2

DB_CONFIG = {
        "dbname": "demo",
        "user": "postgres",
        "password": "Labyrinth",
        "host": "localhost",
        "port": 5432
}

LOG_DIR = "/var/lib/postgresql/data/log"

LOG_PATTERN = re.compile(r"postgresql-(\d{4})-(\d{2})-(\d{2})_\d+\.log")

SEARCH_PATTERN = re.compile(r"Sort Method: external merge\s+Disk:\s+(\d+)([kMG]?B)")
HASH_PATTERN = re.compile(r"Batches.*Memory Usage: \s+(\d+)([kMG]?B)")

one_week_ago = datetime.now() - timedelta(days=7)

def to_bytes(value: int, unit: str) -> int:
    unit = unit.upper()
    if unit == "B":
        return value
    elif unit == "KB":
        return value * 1024
    elif unit == "MB":
        return value * 1024**2
    elif unit == "GB":
        return value * 1024**3
    else:
        raise ValueError(f"Неизвестная единица измерения: {unit}")

results = []

for filename in os.listdir(LOG_DIR):
    match = LOG_PATTERN.match(filename)
    if not match:
        continue
    file_date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    if file_date < one_week_ago:
        continue

    file_path = os.path.join(LOG_DIR, filename)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = SEARCH_PATTERN.search(line)

            if m:
                value, unit = int(m.group(1)), m.group(2)
                bytes_value = to_bytes(value, unit)
                results.append(bytes_value)
                continue
            if "Batches" in line and "Memory Usage" in line:
                m2 = HASH_PATTERN.search(line)
                if m2:
                    value, unit = int(m2.group(1)), m2.group(2)
                    results.append(to_bytes(value, unit))



print("Найдено значений: ", len(results))

if results:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    args_str = ",".join(["(now(), %s)"] * len(results))
    query = f"INSERT INTO service.work_mem_stat(stat_date, memory_value) values {args_str}"

    cur.execute(query, results)

    conn.commit()
    cur.close()
    conn.close()

    print("values are inserted")

else:
    print("no rows for insert")
