import unittest

import numpy as np

from core import (
    cumulative_ltv,
    effective_cpi,
    find_payback_day,
    fit_power_law_retention,
    roas_checkpoints,
    validate_retention_points,
)


class RetentionValidationTests(unittest.TestCase):
    def test_points_are_sorted(self):
        days, retention = validate_retention_points([7, 1, 30], [0.12, 0.35, 0.045])
        np.testing.assert_array_equal(days, [1.0, 7.0, 30.0])
        np.testing.assert_allclose(retention, [0.35, 0.12, 0.045])

    def test_rejects_non_monotonic_retention(self):
        with self.assertRaises(ValueError):
            validate_retention_points([1, 7, 30], [0.35, 0.40, 0.04])

    def test_rejects_duplicate_days(self):
        with self.assertRaises(ValueError):
            validate_retention_points([1, 1, 7], [0.35, 0.30, 0.12])


class GrowthModelTests(unittest.TestCase):
    def test_power_law_fit_is_high_quality_for_sample(self):
        fit = fit_power_law_retention([1, 7, 30], [0.35, 0.12, 0.045])
        self.assertEqual(len(fit.forecast), 180)
        self.assertGreater(fit.r_squared, 0.95)
        self.assertGreater(fit.forecast[0], fit.forecast[-1])

    def test_effective_cpi(self):
        self.assertAlmostEqual(effective_cpi(3.0, 0.20), 2.5)

    def test_cumulative_ltv(self):
        values = cumulative_ltv(
            retention_curve=[0.5, 0.25],
            payer_rate=0.10,
            arppu=10.0,
            platform_cut=0.20,
        )
        np.testing.assert_allclose(values, [0.4, 0.6])

    def test_find_payback_day(self):
        self.assertEqual(find_payback_day([0.4, 0.8, 1.2], 1.0), 3)
        self.assertIsNone(find_payback_day([0.1, 0.2], 1.0))

    def test_roas_checkpoints(self):
        result = roas_checkpoints([1.0, 2.0, 3.0], ecpi=2.0, checkpoints=(1, 3, 7))
        self.assertEqual(result, {1: 0.5, 3: 1.5})


if __name__ == "__main__":
    unittest.main()
