def maintenance_cost(
    true_positives,
    false_positives,
    missed_failures,
    replacement_cost,
    recovery_cost
):
    flagged_drives = true_positives + false_positives

    replacement_cost_total = (
        flagged_drives * replacement_cost
    )

    recovery_cost_total = (
        missed_failures * recovery_cost
    )

    return replacement_cost_total + recovery_cost_total


def break_even_cost(
    tp_a, fp_a, missed_a,
    tp_b, fp_b, missed_b,
    replacement_cost
):
    flagged_a = tp_a + fp_a
    flagged_b = tp_b + fp_b

    replacement_a = flagged_a * replacement_cost
    replacement_b = flagged_b * replacement_cost

    return (
        replacement_a - replacement_b
    ) / (missed_b - missed_a)


# Given values
replacement_cost = 900
missed_failure_cost = 6000

policy_a = maintenance_cost(
    16, 60, 4,
    replacement_cost,
    missed_failure_cost
)

policy_b = maintenance_cost(
    10, 8, 10,
    replacement_cost,
    missed_failure_cost
)

break_even = break_even_cost(
    16, 60, 4,
    10, 8, 10,
    replacement_cost
)

print(f"Policy A annual cost: GHC {policy_a:,.2f}")
print(f"Policy B annual cost: GHC {policy_b:,.2f}")
print(f"Break-even missed-failure cost: GHC {break_even:,.2f}")