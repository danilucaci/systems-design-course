import unittest

from load_model import estimate_load


class LoadModelTests(unittest.TestCase):
    def estimate(self, **overrides):
        inputs = dict(daily_requests=400_000, peak_factor=8, mean_latency_ms=300)
        return estimate_load(**(inputs | overrides))

    def test_reference_workload(self):
        result = self.estimate()
        self.assertAlmostEqual(result["average_rps"], 4.62962962962963)
        self.assertAlmostEqual(result["peak_rps"], 37.03703703703704)
        self.assertAlmostEqual(result["mean_in_flight"], 11.11111111111111)

    def test_slow_dependency_increases_occupancy_tenfold(self):
        normal = self.estimate()
        slow = self.estimate(mean_latency_ms=3_000)
        self.assertEqual(normal["peak_rps"], slow["peak_rps"])
        self.assertAlmostEqual(slow["mean_in_flight"], normal["mean_in_flight"] * 10)

    def test_zero_volume(self):
        self.assertEqual(set(self.estimate(daily_requests=0).values()), {0})

    def test_invalid_assumptions(self):
        cases = [dict(daily_requests=-1), dict(peak_factor=0.5),
                 dict(mean_latency_ms=0), dict(mean_latency_ms=-1)]
        for name in ("daily_requests", "peak_factor", "mean_latency_ms"):
            cases.extend({name: value} for value in (float("nan"), float("inf")))
        for inputs in cases:
            with self.subTest(inputs=inputs), self.assertRaises(ValueError):
                self.estimate(**inputs)

    def test_numeric_overflow(self):
        with self.assertRaises(ValueError):
            self.estimate(daily_requests=1e308, peak_factor=1e308)


if __name__ == "__main__":
    unittest.main()
