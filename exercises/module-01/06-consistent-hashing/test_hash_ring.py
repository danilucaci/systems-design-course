import unittest
from unittest.mock import patch
from hash_ring import HashRing


class HashingTests(unittest.TestCase):
    def test_order_of_configuration_does_not_change_placement(self):
        a=HashRing(['A','B','C']); b=HashRing(['C','A','B'])
        self.assertEqual([a.owner(str(i)) for i in range(200)],[b.owner(str(i)) for i in range(200)])

    def test_addition_only_moves_keys_to_added_node(self):
        old=HashRing(['A','B','C']); new=HashRing(['A','B','C','D'])
        moved=[str(i) for i in range(10000) if old.owner(str(i))!=new.owner(str(i))]
        self.assertTrue(moved)
        self.assertTrue(all(new.owner(key)=='D' for key in moved))

    def test_removal_only_moves_removed_nodes_keys(self):
        old=HashRing(['A','B','C']); new=HashRing(['A','C'])
        for i in range(1000):
            key=str(i)
            if old.owner(key)!='B': self.assertEqual(old.owner(key),new.owner(key))

    def test_single_node_and_invalid_membership(self):
        self.assertEqual(HashRing(['only']).owner('any'),'only')
        for nodes in ([],['A','A'],[''],[1]):
            with self.assertRaises(ValueError): HashRing(nodes)

    def test_successor_boundary_and_wraparound(self):
        values={'1:A:0':10,'1:B:0':20,'between':15,'equal':10,'wrap':25}
        with patch('hash_ring.token',side_effect=values.__getitem__):
            ring=HashRing(['A','B'],virtual_nodes=1)
            self.assertEqual(ring.owner('between'),'B')
            self.assertEqual(ring.owner('equal'),'A')
            self.assertEqual(ring.owner('wrap'),'A')
