#!/usr/bin/env python3
"""
TAO Delegation Portfolio Optimizer - Enhanced Version
Uses dTao API endpoints for comprehensive analysis
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

# Constants
DATA_DIR = "/Users/mohammed/Downloads/TAO/data"
OUTPUT_DIR = "/Users/mohammed/Downloads/TAO"
TOTAL_TAO = 175

# Enhanced credibility research data (compiled from web research + API transparency data)
SUBNET_CREDIBILITY = {
    # HIGH CREDIBILITY (80+) - Doxxed teams, audits, real utility
    64: {
        "name": "Chutes",
        "team_score": 90,  # Rayon Labs: Jon Durbin, Namoray (fully doxxed)
        "audit_score": 75,  # Auditor system, TEE planned
        "security_score": 80,  # TEE implementation, proper validation
        "utility_score": 95,  # Real GPU compute, active users
        "community_score": 90,  # Active Discord, responsive
        "red_flags": [],
        "notes": "Leading serverless AI compute. Rayon Labs (3 subnets). Doxxed founders."
    },
    19: {
        "name": "Nineteen.ai",
        "team_score": 90,  # Rayon Labs
        "audit_score": 70,
        "security_score": 75,
        "utility_score": 85,  # Image generation
        "community_score": 85,
        "red_flags": [],
        "notes": "Rayon Labs image generation subnet."
    },
    8: {
        "name": "Vanta (PTN)",
        "team_score": 95,  # Taoshi Inc: Arrash Yasavolian (company registered)
        "audit_score": 65,
        "security_score": 70,
        "utility_score": 85,  # Real prop trading
        "community_score": 80,
        "red_flags": [],
        "notes": "Decentralized prop trading. Founder: 15+ yrs tech exp."
    },
    3: {
        "name": "Templar",
        "team_score": 85,  # Sam Dare, Covenant team
        "audit_score": 70,
        "security_score": 65,
        "utility_score": 95,  # 2 NeurIPS papers, real training
        "community_score": 80,
        "red_flags": [],
        "notes": "Only subnet with 2 NeurIPS papers. Training 1.2B+ models."
    },
    51: {
        "name": "Lium.io",
        "team_score": 75,  # Fish/Datura team
        "audit_score": 85,  # BITSEC AUDITED
        "security_score": 80,
        "utility_score": 90,  # 500+ H100s, real compute
        "community_score": 80,
        "red_flags": [],
        "notes": "Bitsec audited. 500+ H100 GPUs. AWS of Bittensor."
    },
    60: {
        "name": "Bitsec",
        "team_score": 85,  # Security-focused team
        "audit_score": 100,  # THEY ARE THE AUDITORS
        "security_score": 95,
        "utility_score": 90,  # Found $275M+ vulnerabilities
        "community_score": 80,
        "red_flags": [],
        "notes": "Ecosystem security provider. Essential infrastructure."
    },
    44: {
        "name": "Score Vision",
        "team_score": 75,  # Max Sebti
        "audit_score": 55,
        "security_score": 60,
        "utility_score": 85,  # Real sports data analytics
        "community_score": 75,
        "red_flags": [],
        "notes": "Computer vision for football. Real partnerships."
    },
    62: {
        "name": "Ridges",
        "team_score": 70,  # Shak (partially doxxed)
        "audit_score": 55,
        "security_score": 60,
        "utility_score": 85,  # Coding agents
        "community_score": 75,
        "red_flags": [],
        "notes": "Stillcore Capital invested. Building SWE agents."
    },
    34: {
        "name": "BitMind",
        "team_score": 70,
        "audit_score": 60,
        "security_score": 65,
        "utility_score": 80,
        "community_score": 75,
        "red_flags": [],
        "notes": "AI detection. Good APY performance."
    },

    # MEDIUM CREDIBILITY (60-79)
    120: {
        "name": "Affine",
        "team_score": 65,
        "audit_score": 55,
        "security_score": 60,
        "utility_score": 75,
        "community_score": 65,
        "red_flags": [],
        "notes": "RL platform, uses Chutes for hosting."
    },
    9: {
        "name": "IOTA (Macrocosmos)",
        "team_score": 75,  # Macrocosmos AI
        "audit_score": 60,
        "security_score": 65,
        "utility_score": 85,  # ArXiv paper
        "community_score": 70,
        "red_flags": [],
        "notes": "ArXiv paper. Swarm training architecture."
    },
    4: {
        "name": "Targon",
        "team_score": 70,  # Manifold Inc (GitHub shows)
        "audit_score": 60,
        "security_score": 70,  # Confidential compute focus
        "utility_score": 75,
        "community_score": 70,
        "red_flags": [],
        "notes": "Confidential compute with TEE. Long-running."
    },
    2: {
        "name": "DSperse",
        "team_score": 70,  # Inference Labs
        "audit_score": 60,
        "security_score": 65,
        "utility_score": 75,  # ZK inference
        "community_score": 65,
        "red_flags": [],
        "notes": "Zero-knowledge AI inference."
    },
    12: {
        "name": "Compute Horde",
        "team_score": 65,
        "audit_score": 55,
        "security_score": 60,
        "utility_score": 80,
        "community_score": 70,
        "red_flags": [],
        "notes": "GPU compute marketplace."
    },
    81: {
        "name": "Grail",
        "team_score": 65,  # Part of Covenant
        "audit_score": 55,
        "security_score": 60,
        "utility_score": 70,
        "community_score": 65,
        "red_flags": [],
        "notes": "Post-training/RL. Part of Covenant ecosystem."
    },

    # LOWER CREDIBILITY / NEWER (40-59)
    111: {
        "name": "oneoneone",
        "team_score": 50,
        "audit_score": 45,
        "security_score": 50,
        "utility_score": 55,
        "community_score": 55,
        "red_flags": ["Very high APY - verify sustainability", "Newer subnet"],
        "notes": "High APY but less track record. Use caution."
    },
    43: {
        "name": "Graphite",
        "team_score": 55,
        "audit_score": 50,
        "security_score": 55,
        "utility_score": 60,
        "community_score": 55,
        "red_flags": ["High APY variance"],
        "notes": "High yield but needs monitoring."
    },

    # EXCLUDE / RED FLAGS
    67: {
        "name": "Tenex (DEREGISTERED)",
        "team_score": 0,
        "audit_score": 0,
        "security_score": 0,
        "utility_score": 0,
        "community_score": 0,
        "red_flags": [
            "EXIT SCAM - $2.8M stolen",
            "Pseudonymous team - vanished",
            "No timelock - instant fee change to 99%",
            "DEREGISTERED from network"
        ],
        "notes": "EXIT SCAM. DO NOT DELEGATE."
    },
}

def calculate_credibility_score(subnet_id: int) -> float:
    """Calculate composite credibility score with red flag penalties"""
    if subnet_id not in SUBNET_CREDIBILITY:
        return 45  # Default for unknown subnets

    s = SUBNET_CREDIBILITY[subnet_id]

    base_score = (
        s["team_score"] * 0.20 +
        s["audit_score"] * 0.25 +
        s["security_score"] * 0.25 +
        s["utility_score"] * 0.15 +
        s["community_score"] * 0.15
    )

    red_flags = s.get("red_flags", [])
    if any("EXIT SCAM" in rf or "stolen" in rf.lower() for rf in red_flags):
        base_score = 0
    elif any("single owner" in rf.lower() or "no timelock" in rf.lower() for rf in red_flags):
        base_score *= 0.3
    elif len(red_flags) >= 2:
        base_score *= 0.6
    elif len(red_flags) == 1:
        base_score *= 0.85

    return base_score

def load_all_data() -> Dict:
    """Load all collected API data with enhanced metrics"""
    data = {}

    # Helper to safely convert to float, handling None values
    def safe_float(val, default=0):
        return float(val) if val is not None else default

    # Load subnet data (includes emission, net_flow metrics)
    with open(f"{DATA_DIR}/subnets_latest.json") as f:
        subnets_raw = json.load(f)["data"]
        data["subnets"] = subnets_raw
        # Create subnet lookup by netuid
        data["subnet_metrics"] = {}
        for s in subnets_raw:
            netuid = s.get("netuid")
            if netuid is not None:
                data["subnet_metrics"][netuid] = {
                    "emission": safe_float(s.get("emission")),
                    "net_flow_1_day": safe_float(s.get("net_flow_1_day")),
                    "net_flow_7_days": safe_float(s.get("net_flow_7_days")),
                    "net_flow_30_days": safe_float(s.get("net_flow_30_days")),
                    "registration_cost": safe_float(s.get("registration_cost")) / 1e9,
                }

    # Load validator data (pre-dTao structure)
    with open(f"{DATA_DIR}/validators_latest.json") as f:
        data["validators"] = json.load(f)["data"]

    # Load validator yield data (dTao - real APY)
    with open(f"{DATA_DIR}/validator_yield.json") as f:
        yield_data = json.load(f)["data"]
        # Create lookup by hotkey+netuid
        data["validator_yields"] = {}
        for y in yield_data:
            key = (y["hotkey"]["ss58"], y["netuid"])
            data["validator_yields"][key] = y

    # Load subnet pools (includes fear_and_greed, market_cap, liquidity, price_change)
    with open(f"{DATA_DIR}/subnet_pools.json") as f:
        pools = json.load(f)["data"]
        data["pool_names"] = {p["netuid"]: p.get("name", "Unknown") for p in pools}
        # Enhanced pool metrics for market sentiment analysis
        data["pool_metrics"] = {}
        for p in pools:
            netuid = p.get("netuid")
            if netuid is not None:
                data["pool_metrics"][netuid] = {
                    "name": p.get("name", "Unknown") or "Unknown",
                    "fear_and_greed_index": safe_float(p.get("fear_and_greed_index"), 50),
                    "market_cap": safe_float(p.get("market_cap")),
                    "liquidity": safe_float(p.get("liquidity")),
                    "price_change_1h": safe_float(p.get("price_change_1h")),
                    "price_change_24h": safe_float(p.get("price_change_24h")),
                    "price_change_7d": safe_float(p.get("price_change_7d")),
                    "volume_24h": safe_float(p.get("volume_24h")),
                    "alpha_price": safe_float(p.get("alpha_price")),
                }

    # Load subnet identity for transparency info (optional - may not exist)
    try:
        with open(f"{DATA_DIR}/subnet_identity.json") as f:
            identity_data = json.load(f)["data"]
            data["subnet_identity"] = {s["netuid"]: s for s in identity_data}
    except FileNotFoundError:
        data["subnet_identity"] = {}

    # Load GitHub activity for development signals (optional - may not exist)
    try:
        with open(f"{DATA_DIR}/github_activity.json") as f:
            github_raw = json.load(f)["data"]
            data["github_activity"] = {}
            for g in github_raw:
                netuid = g.get("netuid")
                if netuid is not None:
                    data["github_activity"][netuid] = {
                        "commits_30d": g.get("commits_30d", 0),
                        "contributors": g.get("contributors", 0),
                        "last_commit": g.get("last_commit_at"),
                    }
    except FileNotFoundError:
        data["github_activity"] = {}

    return data

def get_validator_apy(validator: dict, yield_data: dict) -> Tuple[float, float, float]:
    """Get APY data for a validator from yield endpoint"""
    hotkey = validator["hotkey"]["ss58"]
    registrations = validator.get("registrations", [])

    best_30d_apy = 0
    best_7d_apy = 0
    best_netuid = 0

    for netuid in registrations:
        key = (hotkey, netuid)
        if key in yield_data:
            y = yield_data[key]
            apy_30d = float(y.get("thirty_day_apy", 0)) * 100
            apy_7d = float(y.get("seven_day_apy", 0)) * 100

            if apy_30d > best_30d_apy:
                best_30d_apy = apy_30d
                best_7d_apy = apy_7d
                best_netuid = netuid

    return best_30d_apy, best_7d_apy, best_netuid

def calculate_stability_score(validator: dict, apy_30d: float, apy_7d: float,
                               pool_metrics: dict = None, subnet_metrics: dict = None,
                               subnet_id: int = None) -> float:
    """Calculate validator stability score with enhanced market data"""
    nominators = validator.get("nominators", 0)
    stake = float(validator.get("stake", 0)) / 1e9

    # Nominator trust score
    nominator_score = min(100, (nominators / 100) * 100)

    # Stake score (higher = more established)
    stake_score = min(100, (stake / 200000) * 100)

    # APY consistency (7d vs 30d - closer = more stable)
    if apy_30d > 0:
        apy_diff_pct = abs(apy_7d - apy_30d) / apy_30d * 100
        consistency_score = max(0, 100 - apy_diff_pct * 2)
    else:
        consistency_score = 50

    # Market sentiment score (from fear_and_greed_index)
    sentiment_score = 50  # Default neutral
    if pool_metrics and subnet_id and subnet_id in pool_metrics:
        # fear_and_greed: 0=extreme fear, 100=extreme greed
        # We want moderate levels (30-70) for stability
        fgi = pool_metrics[subnet_id].get("fear_and_greed_index", 50)
        if 30 <= fgi <= 70:
            sentiment_score = 80  # Healthy range
        elif 20 <= fgi <= 80:
            sentiment_score = 60  # Acceptable
        else:
            sentiment_score = 40  # Extreme sentiment = higher risk

    # Capital flow score (positive net_flow = healthy)
    flow_score = 50  # Default
    if subnet_metrics and subnet_id and subnet_id in subnet_metrics:
        net_flow_7d = subnet_metrics[subnet_id].get("net_flow_7_days", 0)
        if net_flow_7d > 0:
            flow_score = min(100, 60 + (net_flow_7d / 1000) * 40)
        else:
            flow_score = max(20, 50 + (net_flow_7d / 1000) * 30)

    stability = (
        nominator_score * 0.20 +
        stake_score * 0.20 +
        consistency_score * 0.30 +
        sentiment_score * 0.15 +
        flow_score * 0.15
    )

    return stability

def analyze_all_validators(data: Dict) -> List[dict]:
    """Analyze all validators with enhanced APY data - prioritizing high-credibility subnets"""
    results = []
    pool_metrics = data.get("pool_metrics", {})
    subnet_metrics = data.get("subnet_metrics", {})

    # First pass: Create entries for validators on HIGH-CREDIBILITY subnets (70+)
    high_cred_subnets = [sid for sid, info in SUBNET_CREDIBILITY.items()
                        if calculate_credibility_score(sid) >= 70]

    for v in data["validators"]:
        registrations = v.get("registrations", [])
        if not registrations:
            continue

        hotkey = v["hotkey"]["ss58"]

        # Check each high-credibility subnet this validator is on
        for subnet_id in high_cred_subnets:
            if subnet_id not in registrations:
                continue

            # Get APY for this specific subnet
            key = (hotkey, subnet_id)
            apy_30d = 0
            apy_7d = 0
            if key in data["validator_yields"]:
                y = data["validator_yields"][key]
                apy_30d = float(y.get("thirty_day_apy", 0)) * 100
                apy_7d = float(y.get("seven_day_apy", 0)) * 100

            # If no yield data, use validator's base APR (from validator endpoint)
            if apy_30d == 0:
                # Use apr_30_day_average if available, else base apr
                base_apr = float(v.get("apr_30_day_average", v.get("apr", 0))) * 100
                apy_30d = base_apr * 0.8  # Conservative estimate
                apy_7d = float(v.get("apr_7_day_average", base_apr / 100)) * 100 * 0.8

            subnet_cred = calculate_credibility_score(subnet_id)
            stability = calculate_stability_score(v, apy_30d, apy_7d,
                                                   pool_metrics, subnet_metrics, subnet_id)
            subnet_name = SUBNET_CREDIBILITY[subnet_id]["name"]

            apy_normalized = min(100, (apy_30d / 60) * 100) if apy_30d > 0 else 30
            accumulation = (
                subnet_cred * 0.55 +
                apy_normalized * 0.25 +
                stability * 0.20
            )

            results.append({
                "name": v.get("name", "Unknown") or "Unknown",
                "hotkey": hotkey,
                "rank": v.get("rank", 999),
                "primary_subnet": subnet_id,
                "subnet_name": subnet_name,
                "registrations": registrations,
                "take_rate": float(v.get("take", 0)) * 100,
                "stake_tao": float(v.get("stake", 0)) / 1e9,
                "nominators": v.get("nominators", 0),
                "apy_30d": apy_30d,
                "apy_7d": apy_7d,
                "subnet_credibility": subnet_cred,
                "stability_score": stability,
                "accumulation_score": accumulation
            })

    # Second pass: Add validators by their best APY subnet (for growth/opportunistic tiers)
    seen_hotkeys = {r["hotkey"] for r in results}

    for v in data["validators"]:
        registrations = v.get("registrations", [])
        if not registrations:
            continue

        hotkey = v["hotkey"]["ss58"]
        if hotkey in seen_hotkeys:
            continue  # Already added for high-cred subnet

        # Get best APY subnet
        apy_30d, apy_7d, best_netuid = get_validator_apy(v, data["validator_yields"])
        primary_subnet = best_netuid if best_netuid > 0 else registrations[0]

        subnet_cred = calculate_credibility_score(primary_subnet)
        if subnet_cred < 40:
            continue

        stability = calculate_stability_score(v, apy_30d, apy_7d,
                                               pool_metrics, subnet_metrics, primary_subnet)
        subnet_name = data["pool_names"].get(primary_subnet, f"SN{primary_subnet}")
        if primary_subnet in SUBNET_CREDIBILITY:
            subnet_name = SUBNET_CREDIBILITY[primary_subnet]["name"]

        apy_normalized = min(100, (apy_30d / 60) * 100)
        accumulation = (
            subnet_cred * 0.55 +
            apy_normalized * 0.25 +
            stability * 0.20
        )

        results.append({
            "name": v.get("name", "Unknown") or "Unknown",
            "hotkey": hotkey,
            "rank": v.get("rank", 999),
            "primary_subnet": primary_subnet,
            "subnet_name": subnet_name,
            "registrations": registrations,
            "take_rate": float(v.get("take", 0)) * 100,
            "stake_tao": float(v.get("stake", 0)) / 1e9,
            "nominators": v.get("nominators", 0),
            "apy_30d": apy_30d,
            "apy_7d": apy_7d,
            "subnet_credibility": subnet_cred,
            "stability_score": stability,
            "accumulation_score": accumulation
        })

    # Sort by accumulation score
    results.sort(key=lambda x: x["accumulation_score"], reverse=True)
    return results

def construct_portfolio(ranked_validators: List[dict], total_tao: float = 175) -> dict:
    """Construct diversified portfolio meeting all requirements"""
    portfolio = {
        "core": [],      # 60% - highest credibility
        "growth": [],    # 30% - good credibility + yield
        "opportunistic": []  # 10% - emerging
    }

    max_per_validator = total_tao * 0.40  # 70 TAO
    max_per_subnet = total_tao * 0.50  # 87.5 TAO

    used_subnets = {}
    used_validators = set()

    def can_allocate(validator, amount):
        subnet = validator["primary_subnet"]
        current = used_subnets.get(subnet, 0)
        return current + amount <= max_per_subnet

    def allocate(validator, amount, tier):
        subnet = validator["primary_subnet"]
        used_subnets[subnet] = used_subnets.get(subnet, 0) + amount
        used_validators.add(validator["hotkey"])
        portfolio[tier].append({
            "validator": validator["name"],
            "hotkey": validator["hotkey"],
            "subnet_id": subnet,
            "subnet_name": validator["subnet_name"],
            "allocation_tao": round(amount, 1),
            "apy_30d": validator["apy_30d"],
            "apy_7d": validator["apy_7d"],
            "credibility_score": validator["subnet_credibility"],
            "accumulation_score": validator["accumulation_score"],
            "take_rate": validator["take_rate"],
            "nominators": validator["nominators"],
            "stake_tao": validator["stake_tao"]
        })

    def tier_total(tier):
        return sum(p["allocation_tao"] for p in portfolio[tier])

    # CORE: credibility >= 75 - target 60% (105 TAO)
    core_target = total_tao * 0.60
    core_candidates = [v for v in ranked_validators
                       if v["subnet_credibility"] >= 75 and v["hotkey"] not in used_validators]
    for v in core_candidates:
        if tier_total("core") >= core_target:
            break
        remaining = core_target - tier_total("core")
        amount = min(max_per_validator, 50, remaining)
        if can_allocate(v, amount) and amount >= 15:
            allocate(v, amount, "core")

    # If core underfilled, expand criteria to credibility >= 70
    if tier_total("core") < core_target * 0.8:
        expanded_core = [v for v in ranked_validators
                        if v["subnet_credibility"] >= 70 and v["hotkey"] not in used_validators]
        for v in expanded_core:
            if tier_total("core") >= core_target:
                break
            remaining = core_target - tier_total("core")
            amount = min(max_per_validator, 40, remaining)
            if can_allocate(v, amount) and amount >= 15:
                allocate(v, amount, "core")

    # GROWTH: credibility 60-75 (or 55-70) - target 30% (52.5 TAO)
    growth_target = total_tao * 0.30
    growth_candidates = [v for v in ranked_validators
                        if 55 <= v["subnet_credibility"] < 80
                        and v["hotkey"] not in used_validators]
    # Sort growth candidates by APY (we want yield here)
    growth_candidates.sort(key=lambda x: x["apy_30d"], reverse=True)

    for v in growth_candidates:
        if tier_total("growth") >= growth_target:
            break
        remaining = growth_target - tier_total("growth")
        amount = min(35, remaining)
        if can_allocate(v, amount) and amount >= 10:
            allocate(v, amount, "growth")

    # OPPORTUNISTIC: credibility 45-60 - target 10% (17.5 TAO)
    opp_target = total_tao * 0.10
    opp_candidates = [v for v in ranked_validators
                     if 45 <= v["subnet_credibility"] < 65
                     and v["hotkey"] not in used_validators]
    # Sort by APY for opportunistic (yield play)
    opp_candidates.sort(key=lambda x: x["apy_30d"], reverse=True)

    for v in opp_candidates[:2]:
        if tier_total("opportunistic") >= opp_target:
            break
        remaining = opp_target - tier_total("opportunistic")
        amount = min(20, remaining)
        if can_allocate(v, amount) and amount >= 5:
            allocate(v, amount, "opportunistic")

    # REBALANCE: If any tier underfilled, redistribute to filled tiers
    current_total = tier_total("core") + tier_total("growth") + tier_total("opportunistic")
    if current_total < total_tao:
        shortfall = total_tao - current_total
        # Add to core (safest)
        remaining_core = [v for v in ranked_validators
                         if v["subnet_credibility"] >= 65 and v["hotkey"] not in used_validators]
        for v in remaining_core:
            if shortfall <= 0:
                break
            amount = min(30, shortfall)
            if can_allocate(v, amount) and amount >= 10:
                allocate(v, amount, "growth")  # Add as growth since core is safer
                shortfall -= amount

    return portfolio

def calculate_projections(portfolio: dict) -> dict:
    """Calculate TAO growth projections"""
    total_allocation = 0
    weighted_apy = 0

    for tier in ["core", "growth", "opportunistic"]:
        for pos in portfolio[tier]:
            total_allocation += pos["allocation_tao"]
            weighted_apy += pos["allocation_tao"] * pos["apy_30d"]

    blended_apy = weighted_apy / total_allocation if total_allocation > 0 else 0

    def project_growth(initial: float, apy: float, years: float) -> float:
        monthly_rate = apy / 100 / 12
        months = int(years * 12)
        return initial * ((1 + monthly_rate) ** months)

    projections = {
        "blended_apy": blended_apy,
        "total_allocated": total_allocation,
        "scenarios": {}
    }

    for scenario, adjustment in [("conservative", -10), ("moderate", 0), ("optimistic", 5)]:
        adj_apy = max(10, blended_apy + adjustment)
        projections["scenarios"][scenario] = {
            "apy": adj_apy,
            "6_months": round(project_growth(total_allocation, adj_apy, 0.5), 2),
            "1_year": round(project_growth(total_allocation, adj_apy, 1), 2),
            "2_years": round(project_growth(total_allocation, adj_apy, 2), 2),
            "3_years": round(project_growth(total_allocation, adj_apy, 3), 2),
            "5_years": round(project_growth(total_allocation, adj_apy, 5), 2)
        }

    return projections

def main():
    print("=" * 70)
    print("TAO DELEGATION PORTFOLIO OPTIMIZER - ENHANCED")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # Load data
    print("\n[1/5] Loading API data (including dTao yield endpoints)...")
    data = load_all_data()
    print(f"  - {len(data['subnets'])} subnets")
    print(f"  - {len(data['validators'])} validators")
    print(f"  - {len(data['validator_yields'])} validator yield records")
    print(f"  - {len(data.get('pool_metrics', {}))} subnet pool metrics (sentiment/liquidity)")
    print(f"  - {len(data.get('subnet_metrics', {}))} subnet flow metrics")
    print(f"  - {len(data.get('github_activity', {}))} github activity records")

    # Analyze validators
    print("\n[2/5] Analyzing validators with real APY data...")
    ranked_validators = analyze_all_validators(data)
    print(f"  - {len(ranked_validators)} validators analyzed")

    # Print top 15
    print("\n" + "=" * 80)
    print("TOP 15 VALIDATORS BY ACCUMULATION SCORE")
    print("=" * 80)
    print(f"{'#':<3} {'Name':<22} {'Subnet':<14} {'30d APY':<9} {'Cred':<6} {'Score':<6}")
    print("-" * 80)

    for i, v in enumerate(ranked_validators[:15], 1):
        name = v['name'][:21] if v['name'] else "Unknown"
        print(f"{i:<3} {name:<22} {v['subnet_name'][:13]:<14} "
              f"{v['apy_30d']:>6.1f}%   {v['subnet_credibility']:>4.0f}   {v['accumulation_score']:>5.1f}")

    # Construct portfolio
    print("\n[3/5] Constructing diversified portfolio...")
    portfolio = construct_portfolio(ranked_validators)

    # Calculate projections
    print("\n[4/5] Calculating projections...")
    projections = calculate_projections(portfolio)

    # Print portfolio
    print("\n" + "=" * 80)
    print(f"RECOMMENDED PORTFOLIO ALLOCATION ({TOTAL_TAO} TAO)")
    print("=" * 80)

    total_allocated = 0
    for tier in ["core", "growth", "opportunistic"]:
        tier_total = sum(p["allocation_tao"] for p in portfolio[tier])
        total_allocated += tier_total
        tier_label = {"core": "CORE HOLDINGS (60%)", "growth": "GROWTH HOLDINGS (30%)", "opportunistic": "OPPORTUNISTIC (10%)"}
        print(f"\n{tier_label[tier]} - {tier_total:.1f} TAO:")
        print("-" * 60)
        for p in portfolio[tier]:
            print(f"  → {p['allocation_tao']:.1f} TAO: {p['validator'][:22]}")
            print(f"      Subnet: {p['subnet_name']} | APY: {p['apy_30d']:.1f}% | Cred: {p['credibility_score']:.0f}")

    print(f"\n{'='*60}")
    print(f"TOTAL ALLOCATED: {total_allocated:.1f} TAO")
    print(f"BLENDED 30-DAY APY: {projections['blended_apy']:.1f}%")
    print(f"SUBNETS USED: {len(set(p['subnet_id'] for tier in portfolio.values() for p in tier))}")

    # Print projections
    print("\n" + "=" * 80)
    print("ACCUMULATION PROJECTIONS")
    print("=" * 80)
    print(f"{'Timeframe':<12} {'Conservative':<18} {'Moderate':<18} {'Optimistic':<18}")
    print("-" * 66)

    for tf in ["6_months", "1_year", "2_years", "3_years", "5_years"]:
        label = tf.replace("_", " ").title()
        c = projections["scenarios"]["conservative"][tf]
        m = projections["scenarios"]["moderate"][tf]
        o = projections["scenarios"]["optimistic"][tf]
        print(f"{label:<12} {c:>14.1f} TAO  {m:>14.1f} TAO  {o:>14.1f} TAO")

    print(f"\nScenario APYs: Conservative={projections['scenarios']['conservative']['apy']:.1f}%, "
          f"Moderate={projections['scenarios']['moderate']['apy']:.1f}%, "
          f"Optimistic={projections['scenarios']['optimistic']['apy']:.1f}%")

    # Save outputs
    print("\n[5/5] Saving output files...")

    # Credibility analysis JSON
    cred_output = {
        "analysis_timestamp": datetime.now().isoformat(),
        "methodology": {
            "weights": {
                "team_transparency": 0.20,
                "code_audit": 0.25,
                "smart_contract_security": 0.25,
                "utility_verification": 0.15,
                "community_health": 0.15
            },
            "penalties": {
                "exit_scam": "Total exclusion (score = 0)",
                "single_owner_no_timelock": "70% penalty",
                "multiple_red_flags": "40% penalty",
                "single_red_flag": "15% penalty"
            }
        },
        "subnets_analyzed": {}
    }

    for subnet_id, info in SUBNET_CREDIBILITY.items():
        cred_output["subnets_analyzed"][str(subnet_id)] = {
            **info,
            "composite_credibility_score": calculate_credibility_score(subnet_id),
            "eligible_for_delegation": calculate_credibility_score(subnet_id) >= 50
        }

    with open(f"{OUTPUT_DIR}/credibility_analysis.json", "w") as f:
        json.dump(cred_output, f, indent=2)
    print(f"  - credibility_analysis.json")

    # Portfolio allocation JSON
    portfolio_output = {
        "analysis_timestamp": datetime.now().isoformat(),
        "user_context": {
            "wallet_size_tao": TOTAL_TAO,
            "strategy": "Long-term TAO accumulation",
            "priority": "Capital preservation over yield maximization"
        },
        "portfolio": portfolio,
        "projections": projections,
        "diversification_compliance": {
            "max_per_validator_pct": 40,
            "max_per_subnet_pct": 50,
            "min_subnets": 3,
            "subnets_used": len(set(p["subnet_id"] for tier in portfolio.values() for p in tier)),
            "validators_used": sum(len(tier) for tier in portfolio.values()),
            "tier_allocations": {
                "core_tao": sum(p["allocation_tao"] for p in portfolio["core"]),
                "growth_tao": sum(p["allocation_tao"] for p in portfolio["growth"]),
                "opportunistic_tao": sum(p["allocation_tao"] for p in portfolio["opportunistic"])
            }
        },
        "rebalancing_triggers": [
            "Any subnet credibility drops below 60",
            "Any validator experiences >48hr downtime",
            "Significant emission changes to portfolio subnets",
            "Security incidents or team departures",
            "Quarterly review (regardless of events)"
        ],
        "critical_exclusions": [
            {
                "subnet_id": 67,
                "name": "Tenex",
                "reason": "EXIT SCAM - $2.8M stolen. Deregistered from network."
            }
        ]
    }

    with open(f"{OUTPUT_DIR}/portfolio_allocation.json", "w") as f:
        json.dump(portfolio_output, f, indent=2)
    print(f"  - portfolio_allocation.json")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return {
        "validators": ranked_validators,
        "portfolio": portfolio,
        "projections": projections
    }

if __name__ == "__main__":
    results = main()
