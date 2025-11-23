import time
import random

from signalguard_logs.models import LogRecord, LogStream
from signalguard_logs.recipes import ErrorBurstRecipe


def generate_synthetic_logs(n: int = 400):
    records = []
    now = time.time()
    for i in range(n):
        ts = now + i
        # mostly info logs
        level = "INFO"
        msg = "Request handled successfully"

        # occasional error burst between i 150 and 200
        if 150 <= i <= 200 and random.random() < 0.7:
            level = "ERROR"
            msg = f"Timeout while calling dependency service, attempt={random.randint(1,3)}"

        records.append(
            LogRecord(
                timestamp=ts,
                level=level,
                message=msg,
                service="checkout",
            )
        )
    return LogStream(records)


def main():
    stream = generate_synthetic_logs()
    recipe = ErrorBurstRecipe(service="checkout", level="ERROR", window_size=30.0, baseline_factor=3.0)
    result = recipe.run(stream)

    labels = result["labels"]
    scores = result["scores"]
    s = result["filtered_stream"]

    print("=== ErrorBurstRecipe synthetic demo ===")
    print(f"Filtered records: {len(s.records)}")
    print(f"Anomalous records: {(labels == 1).sum()}")
    print("First 10 anomaly scores:", scores[:10])


if __name__ == "__main__":
    main()
