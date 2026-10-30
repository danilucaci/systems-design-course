import unittest
from decimal import Decimal
from capacity import estimate


class CapacityTests(unittest.TestCase):
    def test_known_workload_with_explicit_units(self):
        result=estimate(500,200,20,1000,30)
        self.assertEqual(result['mean_inflight'],100)
        self.assertEqual(result['logical_bytes'],51840000000)
        self.assertEqual(result['physical_bytes_without_backups'],202176000000)
        self.assertNotEqual(result['logical_GB'],result['logical_GiB'])

    def test_retry_amplifies_capacity_but_not_logical_idempotent_writes(self):
        base=estimate(100,100,5,100,1); retry=estimate(100,100,5,100,1,mean_attempts='1.5')
        self.assertEqual(retry['mean_inflight'],base['mean_inflight']*Decimal('1.5'))
        self.assertEqual(retry['logical_bytes'],base['logical_bytes'])

    def test_rejects_nonphysical_and_nonfinite_inputs(self):
        for kwargs in ({'target_utilization':1},{'mean_attempts':'.5'},{'copies':'1.5'},{'mean_latency_ms':float('nan')},{'record_bytes':-1}):
            args=dict(peak_requests_s=500,mean_latency_ms=200,sustained_writes_s=20,record_bytes=1000,retention_days=30)
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError): estimate(**{**args,**kwargs})
