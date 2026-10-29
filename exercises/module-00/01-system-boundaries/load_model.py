import json
from math import isfinite


def estimate_load(
    *, daily_requests: float, peak_factor: float, mean_latency_ms: float
) -> dict[str, float]:
    for name, value in (
        ("daily_requests", daily_requests),
        ("peak_factor", peak_factor),
        ("mean_latency_ms", mean_latency_ms),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if daily_requests < 0 or peak_factor < 1 or mean_latency_ms <= 0:
        raise ValueError("volume >= 0, peak factor >= 1, latency > 0 required")

    average_rps = daily_requests / 86_400
    peak_rps = average_rps * peak_factor
    mean_in_flight = peak_rps * (mean_latency_ms / 1_000)
    if not all(isfinite(value) for value in (peak_rps, mean_in_flight)):
        raise ValueError("estimate exceeds finite numeric range")
    return {
        "average_rps": average_rps,
        "peak_rps": peak_rps,
        "mean_in_flight": mean_in_flight,
    }


if __name__ == "__main__":
    print(json.dumps(estimate_load(
        daily_requests=400_000, peak_factor=8, mean_latency_ms=300
    ), indent=2))
