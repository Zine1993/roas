from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import curve_fit


@dataclass(frozen=True)
class RetentionFit:
    """Result of a retention-model fit and forecast."""

    days: np.ndarray
    observed: np.ndarray
    forecast_days: np.ndarray
    forecast: np.ndarray
    a: float
    b: float
    r_squared: float


def power_law_retention(t: np.ndarray | float, a: float, b: float):
    """Power-law retention curve R(t) = a * t^b."""
    return a * np.power(t, b)


def validate_retention_points(
    days: Iterable[float],
    retention: Iterable[float],
) -> tuple[np.ndarray, np.ndarray]:
    """Validate and sort cohort retention points.

    Retention values must be expressed as fractions in (0, 1].
    """
    x = np.asarray(list(days), dtype=float)
    y = np.asarray(list(retention), dtype=float)

    if x.shape != y.shape:
        raise ValueError("Day and retention arrays must have the same length.")
    if x.size < 2:
        raise ValueError("At least two retention points are required.")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Retention data must contain only finite numbers.")
    if np.any(x <= 0):
        raise ValueError("Day values must be greater than 0.")
    if np.any(y <= 0) or np.any(y > 1):
        raise ValueError("Retention rates must be greater than 0% and at most 100%.")

    order = np.argsort(x)
    x = x[order]
    y = y[order]

    if np.any(np.diff(x) <= 0):
        raise ValueError("Day values must be unique.")
    if np.any(np.diff(y) > 1e-12):
        raise ValueError(
            "Retention must be non-increasing by day. "
            "Check the cohort points or remove noisy reversals before fitting."
        )

    return x, y


def fit_power_law_retention(
    days: Iterable[float],
    retention: Iterable[float],
    horizon: int = 180,
) -> RetentionFit:
    """Fit a decaying power-law retention curve and forecast to ``horizon``."""
    if horizon < 1:
        raise ValueError("Forecast horizon must be at least 1 day.")

    x, y = validate_retention_points(days, retention)

    initial_a = min(float(y[0]), 0.999999)
    params, _ = curve_fit(
        power_law_retention,
        x,
        y,
        p0=[initial_a, -0.5],
        bounds=([1e-9, -5.0], [1.0, 0.0]),
        maxfev=10000,
    )
    a, b = float(params[0]), float(params[1])

    observed_fit = power_law_retention(x, a, b)
    residual_sum = float(np.sum(np.square(y - observed_fit)))
    total_sum = float(np.sum(np.square(y - np.mean(y))))
    if total_sum <= np.finfo(float).eps:
        r_squared = 1.0 if residual_sum <= np.finfo(float).eps else 0.0
    else:
        r_squared = 1.0 - (residual_sum / total_sum)

    forecast_days = np.arange(1, horizon + 1, dtype=int)
    forecast = np.clip(power_law_retention(forecast_days, a, b), 0.0, 1.0)

    return RetentionFit(
        days=x,
        observed=y,
        forecast_days=forecast_days,
        forecast=forecast,
        a=a,
        b=b,
        r_squared=r_squared,
    )


def effective_cpi(cpi: float, organic_lift: float) -> float:
    """Return effective CPI. ``organic_lift`` is a fraction, e.g. 0.2 for 20%."""
    if cpi <= 0:
        raise ValueError("CPI must be greater than 0.")
    if organic_lift < 0:
        raise ValueError("Organic lift cannot be negative.")
    return float(cpi / (1.0 + organic_lift))


def cumulative_ltv(
    retention_curve: Sequence[float],
    payer_rate: float,
    arppu: float,
    platform_cut: float,
) -> np.ndarray:
    """Calculate cumulative net LTV across a retention curve.

    ``payer_rate`` and ``platform_cut`` are fractions in [0, 1].
    """
    retention = np.asarray(retention_curve, dtype=float)
    if retention.size == 0:
        raise ValueError("Retention curve cannot be empty.")
    if not np.all(np.isfinite(retention)) or np.any(retention < 0) or np.any(retention > 1):
        raise ValueError("Retention curve must contain values between 0 and 1.")
    if not 0 <= payer_rate <= 1:
        raise ValueError("Payer rate must be between 0 and 1.")
    if arppu < 0:
        raise ValueError("ARPPU cannot be negative.")
    if not 0 <= platform_cut < 1:
        raise ValueError("Platform cut must be at least 0 and less than 1.")

    net_daily_revenue = payer_rate * arppu * (1.0 - platform_cut)
    return np.cumsum(retention * net_daily_revenue)


def find_payback_day(cumulative_ltv_values: Sequence[float], ecpi: float) -> int | None:
    """Return the first 1-indexed day where cumulative LTV reaches eCPI."""
    if ecpi <= 0:
        raise ValueError("eCPI must be greater than 0.")
    ltv = np.asarray(cumulative_ltv_values, dtype=float)
    if ltv.size == 0:
        return None

    indices = np.flatnonzero(ltv >= ecpi)
    return int(indices[0] + 1) if indices.size else None


def roas_checkpoints(
    cumulative_ltv_values: Sequence[float],
    ecpi: float,
    checkpoints: Sequence[int] = (7, 14, 30, 60, 90, 180),
) -> dict[int, float]:
    """Return ROAS ratios (1.0 == 100%) for requested day checkpoints."""
    if ecpi <= 0:
        raise ValueError("eCPI must be greater than 0.")

    ltv = np.asarray(cumulative_ltv_values, dtype=float)
    if ltv.size == 0:
        raise ValueError("Cumulative LTV cannot be empty.")

    result: dict[int, float] = {}
    for day in checkpoints:
        if day < 1:
            raise ValueError("ROAS checkpoint days must be at least 1.")
        if day <= ltv.size:
            result[int(day)] = float(ltv[day - 1] / ecpi)
    return result


def break_even_paid_cpi(
    cumulative_ltv_values: Sequence[float],
    organic_lift: float,
    checkpoints: Sequence[int] = (30, 90, 180),
) -> dict[int, float]:
    """Return the maximum paid CPI that breaks even at each checkpoint.

    Because ``eCPI = paid_CPI / (1 + organic_lift)``, the paid CPI that
    corresponds to 100% ROAS at a checkpoint is cumulative LTV multiplied
    by ``1 + organic_lift``.
    """
    if organic_lift < 0:
        raise ValueError("Organic lift cannot be negative.")

    ltv = np.asarray(cumulative_ltv_values, dtype=float)
    if ltv.size == 0:
        raise ValueError("Cumulative LTV cannot be empty.")
    if not np.all(np.isfinite(ltv)) or np.any(ltv < 0):
        raise ValueError("Cumulative LTV must contain finite non-negative values.")

    result: dict[int, float] = {}
    for day in checkpoints:
        if day < 1:
            raise ValueError("Break-even checkpoint days must be at least 1.")
        if day <= ltv.size:
            result[int(day)] = float(ltv[day - 1] * (1.0 + organic_lift))
    return result


def scenario_metrics(
    retention_curve: Sequence[float],
    cpi: float,
    organic_lift: float,
    payer_rate: float,
    arppu: float,
    platform_cut: float,
    checkpoints: Sequence[int] = (30, 90, 180),
) -> dict[str, object]:
    """Calculate payback and ROAS metrics for one deterministic scenario."""
    ecpi = effective_cpi(cpi, organic_lift)
    ltv = cumulative_ltv(retention_curve, payer_rate, arppu, platform_cut)
    return {
        "ecpi": ecpi,
        "payback_day": find_payback_day(ltv, ecpi),
        "roas": roas_checkpoints(ltv, ecpi, checkpoints=checkpoints),
        "cumulative_ltv": ltv,
    }


def one_way_sensitivity(
    retention_curve: Sequence[float],
    base_cpi: float,
    organic_lift: float,
    base_payer_rate: float,
    base_arppu: float,
    platform_cut: float,
    cpi_range: float,
    payer_rate_range: float,
    arppu_range: float,
    checkpoints: Sequence[int] = (30, 90, 180),
) -> list[dict[str, object]]:
    """Build a low/base/high one-way sensitivity table.

    Range values are fractional deviations from the baseline, e.g. ``0.2``
    means +/-20%. Only one assumption changes at a time, which keeps the
    scenario table interpretable and avoids implying probabilistic certainty.
    """
    for name, value in (
        ("CPI range", cpi_range),
        ("Payer-rate range", payer_rate_range),
        ("ARPPU range", arppu_range),
    ):
        if not 0 <= value < 1:
            raise ValueError(f"{name} must be at least 0 and less than 1.")

    if not 0 <= base_payer_rate <= 1:
        raise ValueError("Base payer rate must be between 0 and 1.")
    if base_arppu < 0:
        raise ValueError("Base ARPPU cannot be negative.")

    scenarios: list[tuple[str, str, float, float, float]] = [
        ("Baseline", "Base", base_cpi, base_payer_rate, base_arppu),
        ("CPI", "Low", base_cpi * (1.0 - cpi_range), base_payer_rate, base_arppu),
        ("CPI", "High", base_cpi * (1.0 + cpi_range), base_payer_rate, base_arppu),
        (
            "Payer rate",
            "Low",
            base_cpi,
            max(0.0, base_payer_rate * (1.0 - payer_rate_range)),
            base_arppu,
        ),
        (
            "Payer rate",
            "High",
            base_cpi,
            min(1.0, base_payer_rate * (1.0 + payer_rate_range)),
            base_arppu,
        ),
        (
            "ARPPU",
            "Low",
            base_cpi,
            base_payer_rate,
            base_arppu * (1.0 - arppu_range),
        ),
        (
            "ARPPU",
            "High",
            base_cpi,
            base_payer_rate,
            base_arppu * (1.0 + arppu_range),
        ),
    ]

    rows: list[dict[str, object]] = []
    for metric, scenario, scenario_cpi, payer_rate, arppu in scenarios:
        metrics = scenario_metrics(
            retention_curve=retention_curve,
            cpi=scenario_cpi,
            organic_lift=organic_lift,
            payer_rate=payer_rate,
            arppu=arppu,
            platform_cut=platform_cut,
            checkpoints=checkpoints,
        )
        row: dict[str, object] = {
            "Metric": metric,
            "Scenario": scenario,
            "CPI": float(scenario_cpi),
            "PayerRate": float(payer_rate),
            "ARPPU": float(arppu),
            "eCPI": float(metrics["ecpi"]),
            "PaybackDay": metrics["payback_day"],
        }
        for day, ratio in metrics["roas"].items():
            row[f"D{day}ROAS"] = float(ratio)
        rows.append(row)

    return rows
