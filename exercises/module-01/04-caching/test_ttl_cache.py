import asyncio
import unittest
from ttl_cache import TTLCache, CacheBusy


class CacheTests(unittest.IsolatedAsyncioTestCase):
    async def test_simultaneous_misses_share_one_load(self):
        cache=TTLCache(); calls=0; started=asyncio.Event(); release=asyncio.Event()
        async def load():
            nonlocal calls
            calls+=1; started.set(); await release.wait(); return 'price'
        tasks=[asyncio.create_task(cache.get('station:1',load)) for _ in range(20)]
        await started.wait(); release.set()
        self.assertEqual(await asyncio.gather(*tasks),['price']*20)
        self.assertEqual(calls,1)
        await cache.close()

    async def test_cancelled_waiter_does_not_cancel_shared_load(self):
        cache=TTLCache(); started=asyncio.Event(); release=asyncio.Event()
        async def load(): started.set(); await release.wait(); return 'value'
        first=asyncio.create_task(cache.get('key',load)); await started.wait()
        second=asyncio.create_task(cache.get('key',load)); await asyncio.sleep(0)
        first.cancel()
        with self.assertRaises(asyncio.CancelledError): await first
        release.set(); self.assertEqual(await second,'value'); await cache.close()

    async def test_ttl_and_lru_are_separate_limits(self):
        now=[0]; cache=TTLCache(ttl=5,max_entries=1,clock=lambda:now[0]); calls=0
        async def load():
            nonlocal calls
            calls+=1; return str(calls)
        self.assertEqual(await cache.get('a',load),'1')
        self.assertEqual(await cache.get('a',load),'1')
        now[0]=5
        self.assertEqual(await cache.get('a',load),'2')
        await cache.get('b',load)
        self.assertNotIn('a',cache.entries); await cache.close()

    async def test_failures_are_not_cached(self):
        cache=TTLCache()
        async def fail(): raise RuntimeError('origin unavailable')
        async def succeed(): return 'recovered'
        with self.assertRaises(RuntimeError): await cache.get('key',fail)
        self.assertEqual(await cache.get('key',succeed),'recovered'); await cache.close()

    async def test_admission_rejects_new_keys_while_allowing_existing_waiters(self):
        cache=TTLCache(max_inflight=1); started=asyncio.Event(); release=asyncio.Event()
        async def load(): started.set(); await release.wait(); return 'value'
        first=asyncio.create_task(cache.get('a',load)); await started.wait()
        with self.assertRaises(CacheBusy): await cache.get('b',load)
        await cache.close()
        with self.assertRaises(asyncio.CancelledError): await first

    async def test_rejects_oversized_values_and_invalid_ttl(self):
        for ttl in (0,float('nan'),float('inf')):
            with self.assertRaises(ValueError): TTLCache(ttl=ttl)
        cache=TTLCache(max_value_bytes=2)
        async def load(): return '€'
        with self.assertRaises(ValueError): await cache.get('key',load)
        self.assertFalse(cache.entries); await cache.close()

    async def test_hung_load_times_out_and_releases_admission(self):
        cache=TTLCache(load_timeout=0.01)
        async def stuck(): await asyncio.Event().wait()
        with self.assertRaises(TimeoutError): await cache.get('key',stuck)
        self.assertFalse(cache.pending); self.assertFalse(cache.entries)
        await cache.close()
