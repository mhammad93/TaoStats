# TAO Delegation Portfolio Optimizer

A comprehensive tool for analyzing Bittensor validators and subnets to generate optimized delegation portfolios with emphasis on **capital preservation** and **sustainable TAO accumulation**.

## Background

Following the Tenex (SN67) exit scam that resulted in **$2.8M in delegator losses**, this tool prioritizes credibility assessment and security verification before yield optimization.

## Features

- **Credibility Scoring**: Multi-factor analysis of team transparency, audits, security, utility, and community health
- **Real APY Data**: Integration with dTao API endpoints for accurate yield information
- **Portfolio Construction**: Automated diversification across tiers (Core, Growth, Opportunistic)
- **Risk Management**: Red flag detection and automatic exclusion of suspicious subnets
- **Growth Projections**: Conservative, moderate, and optimistic scenario modeling

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Setup

```bash
# 1. Copy environment template and add your API key
cp .env.example .env
# Edit .env with your Taostats API key

# 2. Source environment variables
source .env
```

### Usage

```bash
# 1. Fetch latest data from Taostats API
python3 fetch_data.py

# 2. Run portfolio analysis
python3 analyze_portfolio.py
```

### Output Files

| File | Description |
|------|-------------|
| `tao_delegation_report.md` | Comprehensive analysis report |
| `credibility_analysis.json` | Structured credibility data |
| `portfolio_allocation.json` | Portfolio recommendation |

## Sample Portfolio Output

For a **175 TAO** wallet (as of January 2026):

| Tier | Validator | Subnet | APY | Credibility | Allocation |
|------|-----------|--------|-----|-------------|------------|
| Core | Polychain | Nineteen.ai (SN19) | 79.0% | A- (80) | 50 TAO |
| Core | Taostats | Lium.io (SN51) | 58.8% | A- (82) | 50 TAO |
| Growth | Unknown | Templar (SN3) | 371.3% | B+ (77) | 35 TAO |
| Growth | Tensorplex Labs | Nineteen.ai (SN19) | 87.9% | A- (80) | 17.5 TAO |
| Opportunistic | Unknown | Hone | 144.2% | C (45) | 17.5 TAO |

**Blended APY:** 140.9% | **Subnets Used:** 4

*Note: APY rates are highly variable and reflect current market conditions.*

## Credibility Scoring Methodology

```
Score = (Team × 20%) + (Audit × 25%) + (Security × 25%) + (Utility × 15%) + (Community × 15%)
```

### Scoring Components

| Component | Weight | What We Verify |
|-----------|--------|----------------|
| Team Transparency | 20% | Doxxed founders, corporate registration |
| Code Audit | 25% | Security audits by Bitsec or equivalent |
| Smart Contract Security | 25% | Timelocks, multisig, upgrade mechanisms |
| Utility Verification | 15% | Real product usage, revenue, partnerships |
| Community Health | 15% | Discord activity, response times |

### Red Flag Penalties

- **Exit scam indicators**: Total exclusion (score = 0)
- **Single owner + no timelock**: 70% penalty
- **Multiple red flags**: 40% penalty

## Portfolio Construction Rules

### Diversification Requirements
- Maximum 40% per validator
- Maximum 50% per subnet
- Minimum 3 different subnets

### Tier Allocation
- **Core (60%)**: Credibility >= 75 - Capital preservation focus
- **Growth (30%)**: Credibility 60-75 - Balanced risk/reward
- **Opportunistic (10%)**: Credibility 45-60 - Higher yield potential

## API Reference

Uses [Taostats API](https://docs.taostats.io) with the following endpoints:

| Endpoint | Purpose | Records |
|----------|---------|---------|
| `/api/subnet/latest/v1` | Subnet metadata with emission/flow metrics | ~129 |
| `/api/validator/latest/v1` | Validator profiles | ~75 (paginated) |
| `/api/dtao/validator/yield/latest/v1` | Real APY data | ~6,100 (paginated) |
| `/api/dtao/pool/latest/v1` | Pool pricing & sentiment metrics | ~129 |
| `/api/dev_activity/latest/v1` | GitHub activity | ~115 (paginated) |

**Note:** The `fetch_data.py` script handles pagination automatically to ensure complete data retrieval.

## Critical Exclusions

| Subnet | Status | Reason |
|--------|--------|--------|
| Tenex (SN67) | **EXCLUDED** | Exit scam - $2.8M stolen |
| oneoneone (SN111) | Avoid | Insufficient track record |
| Graphite (SN43) | Monitor | High APY variance |

## Project Structure

```
TAO/
├── fetch_data.py              # Data collection script (with pagination)
├── analyze_portfolio.py       # Main analysis engine
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── credibility_analysis.json  # Credibility data output
├── portfolio_allocation.json  # Portfolio recommendation output
├── CLAUDE.md                  # Claude Code context
├── README.md                  # This file
└── data/
    ├── subnets_latest.json    # 129 subnets with flow metrics
    ├── validators_latest.json # 75 validators (paginated)
    ├── validator_yield.json   # 6,100+ APY records (paginated)
    ├── subnet_pools.json      # Pool pricing & sentiment
    └── github_activity.json   # 115 dev activity records
```

## Safety Disclaimer

This tool provides analysis and recommendations only. **Always verify information independently before delegating TAO.** The cryptocurrency space carries inherent risks including but not limited to:

- Smart contract vulnerabilities
- Team/project failures
- Market volatility
- Regulatory changes

**Never delegate more than you can afford to lose.**

## Contributing

Contributions welcome! Areas for improvement:

- Historical APY tracking
- Automated monitoring alerts
- Validator uptime integration
- Additional credibility data sources
- Backtesting framework

## License

MIT License

## Acknowledgments

- [Taostats](https://taostats.io) for API access
- [Bitsec](https://bitsec.com) (SN60) for ecosystem security work
- Bittensor community for transparency and research support
