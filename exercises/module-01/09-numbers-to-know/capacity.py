"""Unit-explicit illustrative estimates; Decimal arithmetic avoids binary-float rounding."""
from decimal import Decimal


def positive(value,name,allow_zero=False):
    result=Decimal(str(value))
    if not result.is_finite() or result<0 or (result==0 and not allow_zero): raise ValueError(f'invalid {name}')
    return result


def estimate(peak_requests_s,mean_latency_ms,sustained_writes_s,record_bytes,retention_days,
             copies=3,target_utilization='0.6',mean_attempts=1,storage_overhead_ratio='0.3'):
    peak=positive(peak_requests_s,'peak requests/s'); latency=positive(mean_latency_ms,'mean latency ms')
    writes=positive(sustained_writes_s,'sustained writes/s',True); size=positive(record_bytes,'record bytes')
    days=positive(retention_days,'retention days'); replicas=positive(copies,'copies')
    utilization=positive(target_utilization,'target utilization'); attempts=positive(mean_attempts,'mean attempts')
    overhead=positive(storage_overhead_ratio,'storage overhead',True)
    if utilization>=1 or attempts<1 or replicas!=replicas.to_integral_value(): raise ValueError('invalid utilization, attempts, or copy count')
    effective=peak*attempts; logical=writes*Decimal(86400)*days*size
    return {'attempts_s':effective,'mean_inflight':effective*latency/1000,
            'required_service_capacity_s':effective/utilization,
            'logical_bytes':logical,'physical_bytes_without_backups':logical*replicas*(1+overhead),
            'logical_GB':logical/Decimal(10)**9,'logical_GiB':logical/Decimal(2)**30}


if __name__=='__main__':
    import json
    print(json.dumps({k:str(v) for k,v in estimate(500,200,20,1000,30).items()},indent=2))
