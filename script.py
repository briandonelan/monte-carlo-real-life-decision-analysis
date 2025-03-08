import numpy as np
import polars as pl

N_SIMULATIONS = 10_000
N_MONTHS = 60
ANNUAL_DISCOUNT_RATE = 0.08
MONTHLY_DISCOUNT_RATE = ANNUAL_DISCOUNT_RATE / 12

rng = np.random.default_rng(seed=42)

def discount_factor(month):
    """
    Compute the discount factor for a given month,
    assuming a simple monthly discount rate approach.
    """
    # Simple approach: discount = 1 / (1 + MONTHLY_DISCOUNT_RATE)^(month)
    return (1 + MONTHLY_DISCOUNT_RATE) ** (-month)


def simulate_scenario_b(n_iterations, n_months, rng):

    base_salary_draws = rng.normal(loc=320_000, scale=35_000, size=n_iterations)
    base_salary_draws = np.clip(base_salary_draws, 0, None)  # no negative salary
    monthly_salary_draws = base_salary_draws / 12.0

    cash_flows = np.zeros(n_iterations * n_months)

    extra_health_premium = -50.0

    bonus_fraction = rng.normal(loc=1.0, scale=0.2, size=(n_iterations, 5))
    bonus_fraction = np.clip(bonus_fraction, 0, None)

    for month in range(n_months):
        year_idx = month // 12

        base_component = monthly_salary_draws
        healthcare_component = extra_health_premium

        if (month + 1) % 12 == 0:
            bonus_amount = 0.15 * base_salary_draws * bonus_fraction[:, year_idx]
            total_monthly = base_component + healthcare_component + bonus_amount
        else:
            total_monthly = base_component + healthcare_component

        start_idx = month * n_iterations
        end_idx = start_idx + n_iterations
        cash_flows[start_idx:end_idx] = total_monthly

    return pl.Series("scenario_b", cash_flows)


def simulate_scenario_a(n_iterations, n_months, rng):

    fixed_cost = -400
    llc_cash_flows = np.zeros(n_iterations * n_months)
    months_to_exit_free_paradigm = np.random.randint(3, 9)
    months_to_exit_hourly_paradigm = np.random.randint(4, 9)

    for month in range(n_months):
        if month < months_to_exit_free_paradigm:
            # No revenue, just the cost
            month_revenues = np.zeros(n_iterations)
        if month >= months_to_exit_free_paradigm and month < (months_to_exit_free_paradigm + months_to_exit_hourly_paradigm):
            # hourly model
            starting_hourly_rate = rng.normal(loc=80.0, scale=15.0, size=n_iterations)
            monthly_revenue_growth_rate = rng.normal(loc=5.0, scale=2.0, size=n_iterations)/100.0
            hours_this_month = rng.normal(loc=16.0, scale=4.0, size=n_iterations)
            month_revenues = starting_hourly_rate * (1 + monthly_revenue_growth_rate * (month - months_to_exit_free_paradigm)) * hours_this_month
            # We'll force no negative revenue by maxing with zero
            month_revenues = np.clip(month_revenues, 0, None)
        else:
        #     retainer model
            starting_retainer = rng.normal(loc=10000.0, scale=5000.0, size=n_iterations)
            starting_retainer = np.clip(starting_retainer, 300.0, None)
            retainers_this_month = np.random.randint(low=0, high=6, size=n_iterations)
            month_revenues = starting_retainer * retainers_this_month

        # Add the fixed cost
        net_monthly = month_revenues + fixed_cost

        # Assign to correct location in final array
        start_idx = month * n_iterations
        end_idx = start_idx + n_iterations
        llc_cash_flows[start_idx:end_idx] = net_monthly

    current_salary = 250_000
    monthly_salary = current_salary / 12.0

    bonus_fraction = rng.normal(loc=0.12, scale=0.03, size=n_iterations)
    bonus_fraction = np.clip(bonus_fraction, 0, None)

    cash_flows = np.zeros(n_iterations * n_months)

    for month in range(n_months):
        # base salary for everyone
        base_component = monthly_salary

        if (month + 1) % 12 == 0:
            bonus_amount = current_salary * bonus_fraction
        else:
            bonus_amount = np.zeros(n_iterations)

        total_monthly = base_component + bonus_amount

        start_idx = month * n_iterations
        end_idx = start_idx + n_iterations
        cash_flows[start_idx:end_idx] = total_monthly + llc_cash_flows[start_idx:end_idx]

    return pl.Series("scenario_a", cash_flows)

scenario_b_series = simulate_scenario_b(N_SIMULATIONS, N_MONTHS, rng)
scenario_a_series = simulate_scenario_a(N_SIMULATIONS, N_MONTHS, rng)

df = pl.DataFrame({
    "iteration": np.tile(np.arange(N_SIMULATIONS), N_MONTHS),
    "month": np.repeat(np.arange(N_MONTHS), N_SIMULATIONS),
    "scenario_b": scenario_b_series,
    "scenario_a": scenario_a_series
})

df_melted = df.unpivot(
    index=["iteration", "month"],
    on=["scenario_b", "scenario_a"],
    variable_name="scenario",
    value_name="cash_flow"
)

df_discounted = df_melted.with_columns(
    (pl.col("cash_flow") * pl.col("month").map_batches(discount_factor)).alias("discounted_cf")
)

df_npv = (
    df_discounted
    .group_by(["scenario", "iteration"])
    .agg([
        pl.col("discounted_cf").sum().alias("NPV")
    ])
)

summary_stats = (
    df_npv
    .group_by("scenario")
    .agg([
        pl.col("NPV").mean().alias("mean_NPV"),
        pl.col("NPV").median().alias("median_NPV"),
        pl.col("NPV").quantile(0.05).alias("p5_NPV"),
        pl.col("NPV").quantile(0.95).alias("p95_NPV")
    ])
    .sort(by="scenario")
)

print(summary_stats)
