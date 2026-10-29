import unittest

from concurrency_probe import probe


class ConcurrencyProbeTests(unittest.IsolatedAsyncioTestCase):
    async def test_gate_bounds_active_work_without_dropping_operations(self):
        result = await probe(requests=10, limit=2)
        self.assertEqual(result, {"completed": 10, "maximum_active": 2})

    async def test_serial_and_wide_limits_have_different_overlap(self):
        serial = await probe(requests=10, limit=1)
        wide = await probe(requests=10, limit=10)
        self.assertEqual(serial["maximum_active"], 1)
        self.assertEqual(wide["maximum_active"], 10)
        self.assertEqual(serial["completed"], wide["completed"])

    async def test_empty_workload_does_not_invent_active_work(self):
        self.assertEqual(await probe(requests=0, limit=2), {"completed": 0, "maximum_active": 0})

    async def test_invalid_inputs_fail_before_scheduling(self):
        for requests, limit in ((-1, 2), (10, 0), (10_001, 1), (1, 10_001), (True, 2), (1, 2.5)):
            with self.subTest(requests=requests, limit=limit), self.assertRaises(ValueError):
                await probe(requests, limit)
