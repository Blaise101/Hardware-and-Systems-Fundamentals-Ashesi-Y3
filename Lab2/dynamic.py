def power_at_utilization(p_idle, p_max, u):
    """
    Calculate CPU power at a given utilization.

    P(u) = P_idle + (P_max - P_idle) * u
    """
    return p_idle + (p_max - p_idle) * u


def simulate(readings, p_idle, p_max, interval_hours):
    """
    Calculate energy consumption for:
    1. Always-max power policy
    2. Ondemand-style power policy
    """

    always_max_kwh = sum(
        p_max * interval_hours
        for _ in readings
    ) / 1000

    ondemand_kwh = sum(
        power_at_utilization(p_idle, p_max, u) * interval_hours
        for u in readings
    ) / 1000

    return always_max_kwh, ondemand_kwh


if __name__ == "__main__":

    # CPU utilization readings from Activity 2.1
    readings = [
        0.608, 0.500, 0.523, 0.534, 0.635,
        0.909, 0.730, 0.662, 0.642, 0.563,
        0.572, 0.656, 0.663, 0.616, 0.513,
        0.701, 0.943, 0.781, 0.687, 0.875,
        0.658, 0.771, 0.778, 0.738, 0.733,
        0.924, 0.857, 0.696, 0.760, 0.699,
        0.875, 0.610, 0.713, 0.690, 0.460,
        0.567, 0.514, 0.654, 0.545, 0.546,
        0.467, 0.504, 0.668, 0.515, 0.592,
        0.636, 0.550, 0.635, 0.592, 0.587,
        0.707, 0.622, 0.601, 0.557, 0.672,
        0.574, 0.655, 0.659, 0.581
    ]

    p_idle = 73
    p_max = 95

    interval_hours = 1 / 60

    always_max, ondemand = simulate(
        readings,
        p_idle,
        p_max,
        interval_hours
    )

    saved_pct = (
        1 - ondemand / always_max
    ) * 100

    print(f"Always-max: {always_max:.4f} kWh")
    print(f"Ondemand-style: {ondemand:.4f} kWh")
    print(f"Energy saved: {saved_pct:.1f}%")