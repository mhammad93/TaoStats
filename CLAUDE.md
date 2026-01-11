# TAO Delegation Portfolio Optimizer - Claude Code Context

## Project Overview

This project analyzes Bittensor validators and subnets via the Taostats API to generate optimized delegation portfolios. The primary goal is **sustainable TAO accumulation** with emphasis on **capital preservation** following the Tenex (SN67) exit scam.

## Key Files

### Scripts
- `fetch_data.py` - Data collection script for Taostats API
- `analyze_portfolio.py` - Main analysis engine with credibility scoring and portfolio construction

### Output Files
- `tao_delegation_report.md` - Comprehensive human-readable report
- `credibility_analysis.json` - Structured credibility research data
- `portfolio_allocation.json` - Programmatic portfolio recommendation

### Data Directory (`/data`)
- `subnets_latest.json` - All subnet data (129 subnets) with emission, net_flow metrics
- `validators_latest.json` - Validator profiles (75 validators, paginated)
- `validator_yield.json` - dTao APY data (6,100+ records, paginated)
- `subnet_pools.json` - Pool/pricing data with fear_and_greed_index, liquidity, volume
- `github_activity.json` - Development metrics (115 records, paginated)

## API Configuration

```bash
# Set environment variable before running
export TAOSTATS_API_KEY="your-api-key"
# Or source the .env file
source .env
```

```python
BASE_URL = "https://api.taostats.io/api"
API_KEY = os.environ.get("TAOSTATS_API_KEY")  # From environment
RATE_LIMIT = 60 requests/minute (1.2s delay between calls)
```

### Key Endpoints (with pagination support)
- `/api/subnet/latest/v1` - Subnet data (single page)
- `/api/validator/latest/v1` - Validator data (paginated, ~75 records)
- `/api/dtao/validator/yield/latest/v1` - Real APY data (paginated, ~6,100 records)
- `/api/dtao/pool/latest/v1` - Pool/pricing data with sentiment metrics
- `/api/dev_activity/latest/v1` - GitHub activity (paginated, ~115 records)

**Note:** The `fetch_data.py` script handles pagination automatically to fetch ALL records.

## Credibility Scoring Methodology

```
Credibility = (Team × 0.20) + (Audit × 0.25) + (Security × 0.25) + (Utility × 0.15) + (Community × 0.15)
```

### Red Flag Penalties
- Exit scam indicators: Score = 0 (total exclusion)
- Single owner + no timelock: 70% penalty
- Multiple red flags: 40% penalty
- Single red flag: 15% penalty

## Portfolio Construction Rules

1. **Diversification Requirements**
   - Max 40% per validator
   - Max 50% per subnet
   - Minimum 3 subnets

2. **Tier Allocations**
   - Core (60%): Credibility >= 75
   - Growth (30%): Credibility 60-75
   - Opportunistic (10%): Credibility 45-60

3. **Accumulation Score**
   ```
   Score = (Credibility × 0.55) + (APY_Normalized × 0.25) + (Stability × 0.20)
   ```

4. **Enhanced Stability Score** (uses market data)
   ```
   Stability = (Nominators × 0.20) + (Stake × 0.20) + (APY_Consistency × 0.30)
             + (Sentiment × 0.15) + (Flow × 0.15)
   ```
   - `Sentiment`: Based on `fear_and_greed_index` (30-70 = healthy)
   - `Flow`: Based on `net_flow_7_days` (positive = healthy capital inflow)

## Critical Safety Rules

- **NEVER** recommend subnets with credibility < 60
- **ALWAYS** flag subnets without timelocks
- **EXCLUDE** any subnet showing exit scam indicators
- Weight recent negative news heavily in scoring
- When uncertain, choose capital preservation

## High-Credibility Subnets (Research Verified)

| Subnet | Credibility | Notes |
|--------|-------------|-------|
| Bitsec (SN60) | 91.3 | Ecosystem security auditor |
| Chutes (SN64) | 84.5 | Rayon Labs, doxxed founders |
| Lium.io (SN51) | 81.8 | Bitsec audited, 500+ H100s |
| Nineteen.ai (SN19) | 79.8 | Rayon Labs |
| Vanta (SN8) | 77.5 | Taoshi Inc, registered company |
| Templar (SN3) | 77.0 | 2 NeurIPS papers |

## Excluded Subnets

| Subnet | Reason |
|--------|--------|
| Tenex (SN67) | EXIT SCAM - $2.8M stolen, deregistered |
| oneoneone (SN111) | Insufficient track record, high APY risk |

## Running the Analysis

```bash
# Fetch fresh data
python3 fetch_data.py

# Run analysis
python3 analyze_portfolio.py
```

## Future Improvements

- [ ] Add historical APY tracking
- [ ] Implement automated monitoring alerts
- [ ] Add validator uptime tracking
- [ ] Integrate with wallet for direct delegation
- [ ] Add backtesting against historical data
