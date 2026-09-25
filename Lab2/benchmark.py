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

def storage_benchmark(file_size_mb=100):
  file_name = "benchmark_test_file.bin"

  data = os.urandom(file_size_mb * 1024 * 1024)

  # Write benchmark
  start = time.time()

  with open(file_name, "wb") as f:
    f.write(data)

  write_time = time.time() - start

  # Read benchmark
  start = time.time()

  with open(file_name, "rb") as f:
    f.read()

  read_time = time.time() - start

  # Clean up
  os.remove(file_name)

  write_speed = file_size_mb / write_time
  read_speed = file_size_mb / read_time

  print(
    f"Storage - write: {write_speed:.1f} MB/s, "
    f"read: {read_speed:.1f} MB/s"
  )

  return write_speed, read_speed

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
