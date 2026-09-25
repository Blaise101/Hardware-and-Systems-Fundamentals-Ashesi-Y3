def phantom_load_monthly_kwh(standby_watts, hours_per_day=24):
    kwh_per_day = standby_watts * hours_per_day / 1000
    return kwh_per_day * 30


def ecg_bill_2026(kwh_consumed):
    if kwh_consumed <= 50:
        return kwh_consumed * 0.34
    elif kwh_consumed <= 300:
        return (50 * 0.34) + ((kwh_consumed - 50) * 0.67)
    elif kwh_consumed <= 600:
        return (50 * 0.34) + (250 * 0.67) + ((kwh_consumed - 300) * 0.87)
    else:
        return (
            (50 * 0.34)
            + (250 * 0.67)
            + (300 * 0.87)
            + ((kwh_consumed - 600) * 0.97)
        )


standby_watts = 0.5

monthly_kwh = phantom_load_monthly_kwh(standby_watts)
monthly_cost = ecg_bill_2026(monthly_kwh)

print(f"Monthly phantom load: {monthly_kwh:.2f} kWh")
print(f"Monthly phantom-load cost: GHC {monthly_cost:.2f}")