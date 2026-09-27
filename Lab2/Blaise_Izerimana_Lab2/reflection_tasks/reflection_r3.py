import matplotlib.pyplot as plt

# Lab 1 CPU values
P_static = 73.0
P_max = 95.0
P_dyn = P_max - P_static

T = 10.0
WINDOW = 60.0

# Assume deep-sleep power is 10% of idle power
P_sleep = 0.10 * P_static


def race_energy():
    """
    Complete the job at full speed, then sleep.
    """
    active_time = T
    sleep_time = WINDOW - T

    energy = (
        (P_static + P_dyn) * active_time
        + P_sleep * sleep_time
    )

    return energy


def slow_energy(k, exponent=3, sleep_power=P_sleep):
    """
    Run the job k times slower, then sleep
    for the remaining time.
    """
    active_time = k * T
    sleep_time = WINDOW - active_time

    active_power = P_static + (
        P_dyn / (k ** exponent)
    )

    energy = (
        active_power * active_time
        + sleep_power * sleep_time
    )

    return energy


def print_results(exponent, sleep_power):
    race = (
        (P_static + P_dyn) * T
        + sleep_power * (WINDOW - T)
    )

    print("\n" + "=" * 60)
    print(f"Exponent = {exponent}")
    print(f"P_sleep = {sleep_power:.2f} W")
    print("=" * 60)

    print(f"Race energy: {race:.3f} J")

    for k in range(1, 7):
        energy = slow_energy(
            k,
            exponent,
            sleep_power
        )

        difference = energy - race

        print(
            f"k={k}: "
            f"Slow = {energy:.3f} J | "
            f"Difference from Race = {difference:.3f} J"
        )


def plot_comparison(exponent, sleep_power, title):
    race = (
        (P_static + P_dyn) * T
        + sleep_power * (WINDOW - T)
    )

    k_values = list(range(1, 7))
    slow_values = [
        slow_energy(k, exponent, sleep_power)
        for k in k_values
    ]

    race_values = [race] * len(k_values)

    plt.figure(figsize=(8, 5))

    plt.plot(
        k_values,
        race_values,
        marker="o",
        label="Race to Idle"
    )

    plt.plot(
        k_values,
        slow_values,
        marker="o",
        label="Slow and Steady"
    )

    plt.xlabel("Slowdown Factor (k)")
    plt.ylabel("Total Energy (J)")
    plt.title(title)

    plt.xticks(k_values)
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    # Case 1: exponent = 3, deep sleep
    print_results(3, P_sleep)

    plot_comparison(
        3,
        P_sleep,
        "Race to Idle vs. Slow and Steady (Exponent = 3)"
    )

    # Case 2: exponent = 2, deep sleep
    print_results(2, P_sleep)

    plot_comparison(
        2,
        P_sleep,
        "Race to Idle vs. Slow and Steady (Exponent = 2)"
    )

    # Case 3: exponent = 3, no deep sleep
    print_results(3, P_static)

    plot_comparison(
        3,
        P_static,
        "Race to Idle vs. Slow and Steady (P_sleep = P_static)"
    )

    # Case 4: exponent = 2, no deep sleep
    print_results(2, P_static)

    plot_comparison(
        2,
        P_static,
        "Race to Idle vs. Slow and Steady (Exponent = 2, No Deep Sleep)"
    )