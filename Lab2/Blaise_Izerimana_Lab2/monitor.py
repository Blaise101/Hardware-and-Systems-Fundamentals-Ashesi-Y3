import csv
import time

import matplotlib.pyplot as plt
import psutil


def monitor(duration=60, interval=1):
    timestamps = []
    cpu_readings = []
    mem_readings = []

    start = time.time()

    while time.time() - start < duration:
        cpu = psutil.cpu_percent(interval=interval)
        memory = psutil.virtual_memory().percent

        timestamps.append(time.time() - start)
        cpu_readings.append(cpu)
        mem_readings.append(memory)

    return timestamps, cpu_readings, mem_readings


def save_readings(timestamps, cpu_readings, mem_readings, label):
    filename = f"readings_{label}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Time (s)", "CPU (%)", "Memory (%)"])

        for t, cpu, memory in zip(
            timestamps,
            cpu_readings,
            mem_readings
        ):
            writer.writerow([t, cpu, memory])

    print(f"Readings saved to {filename}")


def plot_usage(timestamps, cpu_readings, mem_readings, label):
    plt.figure(figsize=(10, 5))

    plt.plot(timestamps, cpu_readings, label="CPU %")
    plt.plot(timestamps, mem_readings, label="Memory %")

    plt.title(f"Resource Usage - {label}")
    plt.xlabel("Time (s)")
    plt.ylabel("Usage (%)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"usage_{label}.png")
    plt.show()


if __name__ == "__main__":

    label = input(
        "Enter workload label (idle, browsing, or demanding): "
    ).strip()

    print(f"Starting {label} monitoring for 60 seconds...")

    timestamps, cpu_readings, mem_readings = monitor(
        duration=60,
        interval=1
    )

    save_readings(
        timestamps,
        cpu_readings,
        mem_readings,
        label
    )

    plot_usage(
        timestamps,
        cpu_readings,
        mem_readings,
        label
    )

    print("Monitoring complete.")