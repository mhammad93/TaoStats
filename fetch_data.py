#!/usr/bin/env python3
"""
TAO Delegation Portfolio Optimizer - Data Collection Script
Fetches subnet and validator data from Taostats API
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

# API Configuration
BASE_URL = "https://api.taostats.io/api"
API_KEY = os.environ.get("TAOSTATS_API_KEY")

if not API_KEY:
    print("ERROR: TAOSTATS_API_KEY environment variable not set.")
    print("Set it with: export TAOSTATS_API_KEY='your-api-key'")
    print("Or create a .env file and use: source .env")
    sys.exit(1)

HEADERS = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}
RATE_LIMIT_DELAY = 1.2  # seconds between calls

# Output directory
OUTPUT_DIR = "/Users/mohammed/Downloads/TAO/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def api_call(endpoint, params=None):
    """Make an API call with rate limiting and error handling"""
    url = f"{BASE_URL}/{endpoint}"
    print(f"Fetching: {url}")

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        response.raise_for_status()
        time.sleep(RATE_LIMIT_DELAY)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        time.sleep(RATE_LIMIT_DELAY * 2)  # Extra delay on error
        return None


def api_call_paginated(endpoint, params=None, max_pages=150):
    """Make paginated API calls to fetch ALL records"""
    all_data = []
    page = 1

    if params is None:
        params = {}

    while page <= max_pages:
        params["page"] = page
        url = f"{BASE_URL}/{endpoint}"
        print(f"Fetching: {url} (page {page})")

        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()

            data = result.get("data", [])
            if not data:
                break  # No more data

            all_data.extend(data)

            # Check pagination info
            pagination = result.get("pagination", {})
            total_pages = pagination.get("total_pages", 1)
            current_page = pagination.get("current_page", page)

            print(f"  Page {current_page}/{total_pages}: {len(data)} records (total: {len(all_data)})")

            if current_page >= total_pages:
                break

            page += 1
            time.sleep(RATE_LIMIT_DELAY)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(RATE_LIMIT_DELAY * 2)
            break

    return {"data": all_data, "total_fetched": len(all_data)}

def save_json(data, filename):
    """Save data to JSON file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filepath}")

def fetch_subnets():
    """Fetch all subnet data"""
    print("\n=== Fetching Subnet Data ===")
    data = api_call("subnet/latest/v1")
    if data:
        save_json(data, "subnets_latest.json")
        print(f"Found {len(data.get('data', []))} subnets")
    return data

def fetch_validators():
    """Fetch all validator data with pagination"""
    print("\n=== Fetching Validator Data ===")
    data = api_call_paginated("validator/latest/v1")
    if data and data.get("data"):
        save_json(data, "validators_latest.json")
        print(f"Found {len(data.get('data', []))} validators")
    return data

def fetch_validator_performance():
    """Fetch validator performance metrics - DEPRECATED: endpoint returns 400"""
    print("\n=== Fetching Validator Performance ===")
    print("  Skipping - endpoint not available in current API version")
    return None

def fetch_delegation_data():
    """Fetch delegation/staking data - DEPRECATED: endpoint returns 404"""
    print("\n=== Fetching Delegation Data ===")
    print("  Skipping - endpoint not available in current API version")
    return None

def fetch_subnet_identities():
    """Fetch subnet identity/metadata - DEPRECATED: endpoint returns 404"""
    print("\n=== Fetching Subnet Identities ===")
    # Note: This endpoint appears to be deprecated or moved
    # The subnet info is now embedded in subnets_latest.json
    print("  Skipping - identity data embedded in subnets_latest.json")
    return None

def fetch_validator_yield():
    """Fetch validator yield/APY data from dTao endpoint with pagination"""
    print("\n=== Fetching Validator Yield Data (dTao) ===")
    # FIXED: Correct endpoint is dtao/validator/yield/latest/v1 (not validator/yield/v1)
    data = api_call_paginated("dtao/validator/yield/latest/v1")
    if data and data.get("data"):
        save_json(data, "validator_yield.json")
        print(f"Found {len(data.get('data', []))} yield records")
    return data

def fetch_subnet_pools():
    """Fetch subnet pool data (liquidity info)"""
    print("\n=== Fetching Subnet Pools ===")
    data = api_call("dtao/pool/latest/v1")
    if data:
        save_json(data, "subnet_pools.json")
    return data

def fetch_github_activity():
    """Fetch subnet GitHub development activity with pagination"""
    print("\n=== Fetching GitHub Activity ===")
    data = api_call_paginated("dev_activity/latest/v1")
    if data and data.get("data"):
        save_json(data, "github_activity.json")
        print(f"Found {len(data.get('data', []))} github activity records")
    return data

def main():
    """Main data collection routine"""
    print("=" * 60)
    print("TAO Delegation Portfolio Optimizer - Data Collection")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Fetch all data
    subnets = fetch_subnets()
    validators = fetch_validators()
    validator_perf = fetch_validator_performance()
    delegation = fetch_delegation_data()
    subnet_ids = fetch_subnet_identities()
    validator_yield = fetch_validator_yield()
    subnet_pools = fetch_subnet_pools()
    github = fetch_github_activity()

    # Summary
    print("\n" + "=" * 60)
    print("Data Collection Complete")
    print("=" * 60)

    summary = {
        "collection_timestamp": datetime.now().isoformat(),
        "subnets_count": len(subnets.get('data', [])) if subnets else 0,
        "validators_count": len(validators.get('data', [])) if validators else 0,
        "files_generated": os.listdir(OUTPUT_DIR)
    }
    save_json(summary, "collection_summary.json")

    return summary

if __name__ == "__main__":
    main()
