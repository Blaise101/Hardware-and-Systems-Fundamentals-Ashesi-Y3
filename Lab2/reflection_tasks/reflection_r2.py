import os
import time
import timeit

import psutil


def cpu_intensive_task():
  return [x ** 2 for x in range(10**6)]

def cpu_benchmark():
  cpu_time = timeit.timeit(cpu_intensive_task, number=10)

  print(f"CPU benchmark: {cpu_time:.5f} s for 10 runs")

  return cpu_time



def memory_benchmark():
  before = psutil.virtual_memory()

  large_list = list(range(10**7))

  time.sleep(1)

  during = psutil.virtual_memory()

  del large_list

  time.sleep(1)

  after = psutil.virtual_memory()

  print(
    f"Memory usage - "
    f"before: {before.percent}%, "
    f"during: {during.percent}%, "
    f"after: {after.percent}%"
  )

  print(
    f"Memory - "
    f"before: {before.used / (1024**3):.2f} GB, "
    f"during: {during.used / (1024**3):.2f} GB, "
    f"after: {after.used / (1024**3):.2f} GB"
  )

  return before, during, after

def storage_benchmark(file_size_gb=10, runs=3):
    filename = "r2_large_test_file.bin"

    file_size_bytes = file_size_gb * 1024 * 1024 * 1024
    chunk_size = 1024 * 1024  # 1 MB
    chunk = os.urandom(chunk_size)

    write_results = []
    read_results = []

    for run in range(runs):

        # -------------------------
        # Write benchmark
        # -------------------------
        start = time.perf_counter()

        with open(filename, "wb") as f:
            bytes_written = 0

            while bytes_written < file_size_bytes:
                remaining = file_size_bytes - bytes_written
                data = chunk if remaining >= chunk_size else chunk[:remaining]

                f.write(data)
                bytes_written += len(data)

            f.flush()
            os.fsync(f.fileno())

        write_time = time.perf_counter() - start
        write_speed = (
            file_size_bytes / (1024 * 1024)
        ) / write_time

        write_results.append(write_speed)

        # -------------------------
        # Read benchmark
        # -------------------------
        start = time.perf_counter()

        with open(filename, "rb") as f:
            while f.read(chunk_size):
                pass

        read_time = time.perf_counter() - start
        read_speed = (
            file_size_bytes / (1024 * 1024)
        ) / read_time

        read_results.append(read_speed)

        print(
            f"Run {run + 1}: "
            f"Write = {write_speed:.2f} MB/s, "
            f"Read = {read_speed:.2f} MB/s"
        )

    os.remove(filename)

    return write_results, read_results


def performance_per_watt(benchmark_score, tdp_watts):
    return benchmark_score / tdp_watts


cpus = {
    "Intel Core i5-7300U": (2358, 15),
    "Intel Core i5-8250U": (3169, 15),
    "Intel Core i5-10210U": (3996, 15),
}


def compare_cpus():
    print("\nPerformance per Watt:")

    for name, (score, tdp) in cpus.items():
        ppw = performance_per_watt(score, tdp)
        print(f"{name}: {ppw:.2f} points/W")


if __name__ == "__main__":
    cpu_benchmark()
    memory_benchmark()
    storage_benchmark()
    compare_cpus()
