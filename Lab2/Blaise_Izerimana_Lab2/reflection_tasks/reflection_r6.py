lab1_cpu_power = 84.00
lab1_monthly_energy = 42.84
lab1_monthly_cost = 14.57

idle_power = 73.0
max_power = 95.0
average_utilization = 0.652

# Lab 2 utilization-based CPU power
lab2_cpu_power = idle_power + (
    (max_power - idle_power) * average_utilization
)

# Keep the same usage assumption as Lab 1
lab2_monthly_energy = (
    lab1_monthly_energy * lab2_cpu_power / lab1_cpu_power
)

# Same tariff basis as Lab 1
lab2_monthly_cost = (
    lab1_monthly_cost * lab2_monthly_energy / lab1_monthly_energy
)

power_difference = (
    (lab2_cpu_power - lab1_cpu_power)
    / lab1_cpu_power * 100
)

energy_difference = (
    (lab2_monthly_energy - lab1_monthly_energy)
    / lab1_monthly_energy * 100
)

cost_difference = (
    (lab2_monthly_cost - lab1_monthly_cost)
    / lab1_monthly_cost * 100
)

print(f"Lab 2 CPU power: {lab2_cpu_power:.2f} W")
print(f"Lab 2 monthly CPU energy: {lab2_monthly_energy:.2f} kWh")
print(f"Lab 2 monthly CPU cost: GHC {lab2_monthly_cost:.2f}")
print(f"Power difference: {power_difference:.2f}%")
print(f"Energy difference: {energy_difference:.2f}%")
print(f"Cost difference: {cost_difference:.2f}%")