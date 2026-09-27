import csv
import re
import subprocess
from datetime import datetime


def get_smart_data(device):
    result = subprocess.run(
        ["smartctl", "-a", device],
        check=False, capture_output=True,
        text=True
    )
    return result.stdout


def parse_smart_data(smart_data):
    patterns = {
        "Raw_Read_Error_Rate":
            r"^\s*1\s+Raw_Read_Error_Rate\s+.*?\s(\d+)\s*$",

        "Reallocate_NAND_Blk_Cnt":
            r"^\s*5\s+Reallocate_NAND_Blk_Cnt\s+.*?\s(\d+)\s*$",

        "Power_On_Hours":
            r"^\s*9\s+Power_On_Hours\s+.*?\s(\d+)\s*$",

        "Power_Cycle_Count":
            r"^\s*12\s+Power_Cycle_Count\s+.*?\s(\d+)\s*$",

        "Temperature_Celsius":
            r"^\s*194\s+Temperature_Celsius\s+(?:\S+\s+){7}(\d+)",

        "Offline_Uncorrectable":
            r"^\s*198\s+Offline_Uncorrectable\s+.*?\s(\d+)\s*$",

        "UDMA_CRC_Error_Count":
            r"^\s*199\s+UDMA_CRC_Error_Count\s+.*?\s(\d+)\s*$"
    }

    attributes = {}

    for name, pattern in patterns.items():
        match = re.search(pattern, smart_data, re.MULTILINE)

        if match:
            attributes[name] = int(match.group(1))

    return attributes


def log_smart_data(attributes, filename="smart_log.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = False

    try:
        with open(filename, "r"):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(filename, "a", newline="") as file:
        fieldnames = [
            "Timestamp",
            "Raw_Read_Error_Rate",
            "Reallocate_NAND_Blk_Cnt",
            "Power_On_Hours",
            "Power_Cycle_Count",
            "Temperature_Celsius",
            "Offline_Uncorrectable",
            "UDMA_CRC_Error_Count"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row = {"Timestamp": timestamp}
        row.update(attributes)

        writer.writerow(row)

    print(f"S.M.A.R.T. data logged at {timestamp}")


if __name__ == "__main__":
    device = "/dev/sda"

    smart_data = get_smart_data(device)
    attributes = parse_smart_data(smart_data)

    print("Current S.M.A.R.T. attributes:")

    for name, value in attributes.items():
        print(f"{name}: {value}")

    log_smart_data(attributes)