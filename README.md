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
pip install requests
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

For a **175 TAO** wallet:

| Tier | Validator | Subnet | APY | Credibility | Allocation |
|------|-----------|--------|-----|-------------|------------|
| Core | tao5 | Bitsec (SN60) | 14.9% | A (91.3) | 50 TAO |
| Core | Unknown | Chutes (SN64) | 13.4% | A- (84.5) | 50 TAO |
| Growth | Cortex Foundation | Vanta (SN8) | 17.6% | B+ (77.5) | 35 TAO |
| Growth | Cortex Foundation | Templar (SN3) | 17.6% | B+ (77.0) | 17.5 TAO |
| Opportunistic | tao.bot | Root (SN0) | 7.0% | C (45.0) | 17.5 TAO |

**Blended APY:** 14.5% | **5-Year Projection:** 349 TAO (+105%)

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

| Endpoint | Purpose |
|----------|---------|
| `/api/subnet/latest/v1` | Subnet metadata |
| `/api/validator/latest/v1` | Validator profiles |
| `/api/dtao/validator/yield/latest/v1` | Real APY data |
| `/api/subnet/identity/v1` | Team/GitHub info |
| `/api/dtao/pool/latest/v1` | Pool pricing |

## Critical Exclusions

| Subnet | Status | Reason |
|--------|--------|--------|
| Tenex (SN67) | **EXCLUDED** | Exit scam - $2.8M stolen |
| oneoneone (SN111) | Avoid | Insufficient track record |
| Graphite (SN43) | Monitor | High APY variance |

## Project Structure

```
TAO/
├── fetch_data.py              # Data collection script
├── analyze_portfolio.py       # Main analysis engine
├── tao_delegation_report.md   # Human-readable report
├── credibility_analysis.json  # Credibility data
├── portfolio_allocation.json  # Portfolio recommendation
├── CLAUDE.md                  # Claude Code context
├── README.md                  # This file
└── data/
    ├── subnets_latest.json
    ├── validators_latest.json
    ├── validator_yield.json
    ├── subnet_identity.json
    ├── subnet_pools.json
    └── github_activity.json
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
