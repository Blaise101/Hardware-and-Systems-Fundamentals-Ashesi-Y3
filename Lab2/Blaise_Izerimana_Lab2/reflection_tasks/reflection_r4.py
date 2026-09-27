import csv
import re
import subprocess
import time

import matplotlib.pyplot as plt
import psutil

DURATION = 300          # 5 minutes
INTERVAL = 1
OUTPUT_FILE = "r4_results.csv"


def cpu_task():
    total = 0
    for i in range(2_000_000):
        total += i ** 2
    return total


def get_drive_temperature():
    try:
        result = subprocess.run(
            ["smartctl", "-A", "/dev/sda"],
            check=False, capture_output=True,
            text=True
        )

        match = re.search(
            r"Temperature_Celsius\s+.*?\s(\d+)\s*$",
            result.stdout,
            re.MULTILINE
        )

        if match:
            return int(match.group(1))

    except Exception:
        pass

    return None


def run_test(condition):
    print("\n" + "=" * 60)
    print(f"CONDITION: {condition}")
    print("=" * 60)

    print("Starting CPU load...")
    print("Duration: 5 minutes")

    readings = []

    start_time = time.perf_counter()

    while time.perf_counter() - start_time < DURATION:

        timestamp = time.perf_counter() - start_time

        cpu_usage = psutil.cpu_percent(interval=0.1)

        freq = psutil.cpu_freq()
        frequency = freq.current if freq else None

        readings.append({
            "time": timestamp,
            "cpu_usage": cpu_usage,
            "frequency": frequency
        })

        # Keep CPU busy between measurements
        task_start = time.perf_counter()

        while time.perf_counter() - task_start < 0.9:
            cpu_task()

    return readings


def save_results(condition, readings):
    filename = condition.replace(" ", "_").lower() + ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Time_s",
            "CPU_Usage_percent",
            "CPU_Frequency_MHz"
        ])

        for row in readings:
            writer.writerow([
                f"{row['time']:.2f}",
                f"{row['cpu_usage']:.2f}",
                f"{row['frequency']:.2f}"
                if row["frequency"] is not None else ""
            ])

    print(f"Saved: {filename}")


def plot_results(results_a, results_b):

    plt.figure(figsize=(10, 5))

    plt.plot(
        [r["time"] for r in results_a],
        [r["frequency"] for r in results_a],
        label="Condition A"
    )

    plt.plot(
        [r["time"] for r in results_b],
        [r["frequency"] for r in results_b],
        label="Condition B"
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU Frequency (MHz)")
    plt.title("CPU Frequency During Sustained Load")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    plt.figure(figsize=(10, 5))

    plt.plot(
        [r["time"] for r in results_a],
        [r["cpu_usage"] for r in results_a],
        label="Condition A"
    )

    plt.plot(
        [r["time"] for r in results_b],
        [r["cpu_usage"] for r in results_b],
        label="Condition B"
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU Utilization (%)")
    plt.title("CPU Utilization During Sustained Load")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    print("\nCONDITION A")
    print("Place laptop on a hard, open surface.")
    input("Press ENTER when ready...")

    temp_before_a = get_drive_temperature()
    print(f"Drive temperature before: {temp_before_a} C")

    results_a = run_test(
        "Condition A - Hard Open Surface"
    )

    temp_after_a = get_drive_temperature()
    print(f"Drive temperature after: {temp_after_a} C")

    save_results(
        "Condition_A_Hard_Surface",
        results_a
    )

    print("\nAllow the laptop to return to normal temperature.")
    input("Press ENTER when ready for Condition B...")

    temp_before_b = get_drive_temperature()
    print(f"Drive temperature before: {temp_before_b} C")

    results_b = run_test(
        "Condition B - Warmer Environment"
    )

    temp_after_b = get_drive_temperature()
    print(f"Drive temperature after: {temp_after_b} C")

    save_results(
        "Condition_B_Warmer_Environment",
        results_b
    )

    print("\nGenerating plots...")
    plot_results(results_a, results_b)