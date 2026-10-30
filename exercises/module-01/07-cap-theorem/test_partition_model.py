import unittest
from partition_model import Register, Unavailable


class PartitionTests(unittest.TestCase):
    def test_cp_rejects_isolated_replica_instead_of_returning_stale_success(self):
        register=Register('cp'); register.partition(); register.write('A',1)
        with self.assertRaises(Unavailable): register.read('B')
        with self.assertRaises(Unavailable): register.write('B',2)
        register.heal(); self.assertEqual(register.read('B'),1)

    def test_ap_successful_read_can_violate_real_time_order(self):
        register=Register('ap'); register.partition(); register.write('A',1)
        self.assertEqual(register.read('B'),0)
        register.heal(); self.assertEqual(register.read('B'),1)

    def test_deterministic_merge_converges_but_discards_one_concurrent_intent(self):
        register=Register('ap'); register.partition(); register.write('A',10); register.write('B',20)
        register.heal()
        self.assertEqual(register.read('A'),register.read('B'))
        self.assertEqual(register.read('A'),20)

    def test_connected_fixed_primary_forwards_reads_and_writes(self):
        register=Register('cp'); register.write('B',3)
        self.assertEqual(register.read('A'),3)
