import os
import statistics
import time


def cpu_task():
    [x ** 2 for x in range(10**6)]


def cpu_benchmark(runs=10):
    results = []

    for _ in range(runs):
        start = time.perf_counter()
        cpu_task()
        elapsed = time.perf_counter() - start
        results.append(elapsed)

    return results


def storage_benchmark(file_size_mb=100, runs=10):
    filename = "r1_test_file.bin"
    data = os.urandom(file_size_mb * 1024 * 1024)

    write_results = []
    read_results = []

    for _ in range(runs):

        # Write
        start = time.perf_counter()

        with open(filename, "wb") as f:
            f.write(data)

        write_time = time.perf_counter() - start
        write_results.append(file_size_mb / write_time)

        # Read
        start = time.perf_counter()

        with open(filename, "rb") as f:
            f.read()

        read_time = time.perf_counter() - start
        read_results.append(file_size_mb / read_time)

    os.remove(filename)

    return write_results, read_results


def statistics_for(values):
    mean = statistics.mean(values)
    standard_deviation = statistics.stdev(values)
    coefficient_of_variation = (
        standard_deviation / mean
    ) * 100

    return mean, standard_deviation, coefficient_of_variation


def print_results(name, values, unit):

    print(f"\n{name}")

    for i, value in enumerate(values, 1):
        print(f"Run {i}: {value:.6f} {unit}")

    mean, std, cv = statistics_for(values)

    print(f"Mean: {mean:.6f} {unit}")
    print(f"Standard deviation: {std:.6f} {unit}")
    print(f"Coefficient of variation: {cv:.2f}%")


def run_condition(condition):

    print("\n" + "=" * 60)
    print(f"CONDITION: {condition}")
    print("=" * 60)

    cpu_results = cpu_benchmark()

    write_results, read_results = storage_benchmark()

    print_results(
        "CPU Time",
        cpu_results,
        "s"
    )

    print_results(
        "Storage Write Speed",
        write_results,
        "MB/s"
    )

    print_results(
        "Storage Read Speed",
        read_results,
        "MB/s"
    )


if __name__ == "__main__":

    run_condition("Condition A - Normal State")