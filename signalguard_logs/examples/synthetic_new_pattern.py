import time
import random

from signalguard_logs.models import LogRecord, LogStream
from signalguard_logs.recipes import NewErrorPatternRecipe


def generate_synthetic_logs():
    records = []
    now = time.time()

    stable_patterns = [
        "Failed to connect to database <NUM>",
        "User <NUM> not found in cache",
        "Invalid credentials for user <NUM>",
    ]

    # initial known patterns
    for i in range(100):
        ts = now + i
        template = random.choice(stable_patterns)
        msg = template.replace("<NUM>", str(random.randint(1, 1000)))
        records.append(LogRecord(timestamp=ts, level="ERROR", message=msg, service="auth"))

    # introduce a new pattern
    for i in range(100, 130):
        ts = now + i
        msg = f"JWT validation failed for token {random.randrange(10**10, 10**12)}"
        records.append(LogRecord(timestamp=ts, level="ERROR", message=msg, service="auth"))

    return LogStream(records)


def main():
    stream = generate_synthetic_logs()

    recipe = NewErrorPatternRecipe(service="auth", level="ERROR")
    result = recipe.run(stream)

    labels = result["labels"]
    scores = result["scores"]
    s = result["filtered_stream"]

    new_count = (labels == 1).sum()
    print("=== NewErrorPatternRecipe synthetic demo ===")
    print(f"Total error logs: {len(s.records)}")
    print(f"New pattern logs: {new_count}")

    # Show a few example messages that were flagged
    print("\nSample anomalies:")
    for rec, label in zip(s.records, labels):
        if label == 1:
            print("  ", rec.message)
            new_count -= 1
            if new_count <= 3:
                break


if __name__ == "__main__":
    main()
