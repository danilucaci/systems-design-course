"""Deterministic placement only: no replication, failure detector, or data transfer."""
import bisect
import hashlib


def token(value): return int.from_bytes(hashlib.sha256(value.encode('utf-8')).digest(),'big')


class HashRing:
    def __init__(self,nodes,virtual_nodes=128):
        nodes=list(nodes)
        if not nodes or any(not isinstance(n,str) or not n for n in nodes) or len(set(nodes))!=len(nodes):
            raise ValueError('nonempty unique node names required')
        if not isinstance(virtual_nodes,int) or virtual_nodes < 1: raise ValueError('positive virtual-node count required')
        points=[]
        for node in sorted(nodes):
            for index in range(virtual_nodes):
                # Length prefix prevents ambiguities between node names and replica numbers.
                position=token(f'{len(node.encode())}:{node}:{index}')
                points.append((position,node))
        points.sort()
        if len({point[0] for point in points})!=len(points): raise ValueError('token collision: choose a new placement configuration')
        self.points=points
        self.positions=[point[0] for point in points]

    def owner(self,key):
        index=bisect.bisect_left(self.positions,token(key))%len(self.points)
        return self.points[index][1]


if __name__ == '__main__':
    from collections import Counter
    keys=[f'journey:{index}' for index in range(10000)]
    old=HashRing(['A','B','C']); new=HashRing(['A','B','C','D'])
    print('Owners after expansion:',dict(Counter(new.owner(key) for key in keys)))
    print('Moved keys:',sum(old.owner(key)!=new.owner(key) for key in keys),'of',len(keys))
