from dataclasses import dataclass

@dataclass
class APIContext:
    """Stores API context and business importance"""
    name: str
    criticality: float  # 0-1 scale
    business_impact: float  # 0-1 scale
    baseline_traffic: float
    expected_latency: float
    error_threshold: float