"""Sequential freeze/copy/fence model, not a live database migration tool."""
import hashlib
from dataclasses import dataclass


class Unavailable(Exception): pass
class StaleRoute(Exception): pass


@dataclass(frozen=True)
class Route:
    bucket: int
    shard: str
    epoch: int


class ShardedStore:
    def __init__(self, buckets=16):
        if not isinstance(buckets,int) or buckets < 1: raise ValueError('positive bucket count required')
        self.buckets=buckets
        self.owners={i:Route(i,'A' if i%2==0 else 'B',1) for i in range(buckets)}
        self.data={'A':{},'B':{},'C':{}}
        self.frozen=set(); self.prepared={}; self.directory_available=True

    def bucket(self,key): return int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],'big')%self.buckets

    def route(self,key):
        if not self.directory_available: raise Unavailable('authoritative directory unreachable')
        return self.owners[self.bucket(key)]

    def check(self,key,route):
        current=self.route(key)
        if route != current: raise StaleRoute('refresh ownership and retry safely')
        if current.bucket in self.frozen: raise Unavailable('bucket migration is frozen')

    def write(self,key,value,route):
        self.check(key,route); self.data[route.shard][key]=value

    def read(self,key,route):
        self.check(key,route); return self.data[route.shard].get(key)

    def freeze(self,bucket):
        if not self.directory_available: raise Unavailable('directory unreachable')
        if bucket not in self.owners or bucket in self.frozen: raise ValueError('invalid or already frozen bucket')
        self.frozen.add(bucket)

    def copy(self,bucket,target):
        if bucket not in self.frozen or target not in self.data or target==self.owners[bucket].shard:
            raise ValueError('freeze a bucket and choose another existing shard')
        source=self.owners[bucket].shard
        snapshot={k:v for k,v in self.data[source].items() if self.bucket(k)==bucket}
        for key in list(self.data[target]):
            if self.bucket(key)==bucket: del self.data[target][key]
        self.data[target].update(snapshot)
        self.prepared[bucket]=target

    def cutover(self,bucket):
        if not self.directory_available: raise Unavailable('directory unreachable')
        if bucket not in self.frozen or bucket not in self.prepared: raise ValueError('copy before cutover')
        old=self.owners[bucket]
        self.owners[bucket]=Route(bucket,self.prepared.pop(bucket),old.epoch+1)
        self.frozen.remove(bucket)

    def abort(self,bucket):
        if not self.directory_available: raise Unavailable('directory unreachable')
        self.prepared.pop(bucket,None); self.frozen.discard(bucket)
