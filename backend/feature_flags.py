"""
Feature flags for Loan Markets features
"""
from typing import Dict
import os

# Feature flags configuration
FEATURE_FLAGS: Dict[str, bool] = {
    "MARKET_INTEL": os.getenv("FEATURE_MARKET_INTEL", "true").lower() == "true",
    "TRANSFER_SIM": os.getenv("FEATURE_TRANSFER_SIM", "true").lower() == "true",
    "LMA_DEVIATION": os.getenv("FEATURE_LMA_DEVIATION", "true").lower() == "true",
    "BUYER_FIT": os.getenv("FEATURE_BUYER_FIT", "true").lower() == "true",
    "NEGOTIATION": os.getenv("FEATURE_NEGOTIATION", "true").lower() == "true",
    "MONITORING": os.getenv("FEATURE_MONITORING", "true").lower() == "true",
    "AUCTION": os.getenv("FEATURE_AUCTION", "true").lower() == "true",
    "DEMO_MODE": os.getenv("FEATURE_DEMO_MODE", "true").lower() == "true",
}


def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURE_FLAGS.get(feature, False)


def get_enabled_features() -> Dict[str, bool]:
    """Get all feature flags"""
    return FEATURE_FLAGS.copy()

