# Zeru Credit Scoring - Methodology

## Objective
To assign a decentralized, explainable credit score (0–100) to wallets based on Compound V2 activity.

## Data Used
We selected the 3 largest transaction logs: deposits, borrows, and liquidations. These reflect key financial behaviors.

## Features
Wallet-level metrics:
- Total deposits/borrows/liquidations
- Transaction counts
- Active days (wallet longevity)
- Ratios: deposit/borrow and liquidation/borrow

## Scoring Logic
We used rule-based scoring:
- Reward high deposit/borrow ratio
- Penalize frequent liquidations
- Favor wallets with long active histories
- Normalize all features, then calculate score as a weighted sum

## Result
Each wallet receives a score between 0–100 reflecting responsible and sustainable behavior.
