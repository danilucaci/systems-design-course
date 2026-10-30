"""Bounded, single-event-loop cache. It does not coordinate separate API processes."""
import asyncio
import math
import time
from collections import OrderedDict


class CacheBusy(Exception): pass


class TTLCache:
    def __init__(self, ttl=30.0, max_entries=128, max_inflight=8, max_value_bytes=4096, load_timeout=1.0, clock=time.monotonic):
        limits=(max_entries,max_inflight,max_value_bytes)
        if not math.isfinite(ttl) or ttl <= 0 or not math.isfinite(load_timeout) or load_timeout <= 0 or any(type(n) is not int or n < 1 for n in limits):
            raise ValueError('positive finite TTL and positive limits required')
        self.ttl, self.max_entries, self.max_inflight = ttl,max_entries,max_inflight
        self.max_value_bytes,self.clock=max_value_bytes,clock
        self.load_timeout=load_timeout
        self.entries=OrderedDict()
        self.pending={}
        self.closed=False

    async def get(self, key, loader):
        if self.closed: raise RuntimeError('cache is closed')
        if not isinstance(key,str) or not 0 < len(key) <= 256: raise ValueError('key must contain 1–256 characters')
        entry=self.entries.get(key)
        if entry and entry[0] > self.clock():
            self.entries.move_to_end(key)
            return entry[1]
        self.entries.pop(key,None)
        task=self.pending.get(key)
        if task is None:
            if len(self.pending) >= self.max_inflight: raise CacheBusy('too many distinct origin loads')
            async def fill():
                try:
                    value=await asyncio.wait_for(loader(),timeout=self.load_timeout)
                    if not isinstance(value,str) or len(value.encode()) > self.max_value_bytes:
                        raise ValueError('loader must return a bounded UTF-8 string')
                    self.entries[key]=(self.clock()+self.ttl,value)
                    self.entries.move_to_end(key)
                    while len(self.entries)>self.max_entries: self.entries.popitem(last=False)
                    return value
                finally:
                    self.pending.pop(key,None)
            task=asyncio.create_task(fill())
            # Retrieve errors even if every waiting caller has disconnected.
            task.add_done_callback(lambda done: done.exception() if not done.cancelled() else None)
            self.pending[key]=task
        return await asyncio.shield(task)

    async def close(self):
        self.closed=True
        tasks=list(self.pending.values())
        for task in tasks: task.cancel()
        await asyncio.gather(*tasks,return_exceptions=True)
        self.pending.clear()
        self.entries.clear()
