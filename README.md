# AI-Powered Decentralized Credit Scoring System

## Description
This project implements an AI-powered decentralized credit scoring system using Compound V2 raw transaction data. The system evaluates wallets based on their deposit, borrow, and liquidation behavior. It processes data from three main transaction types: deposits, borrows, and liquidations. 

## Features
- **Data Processing**: Handles CSV files containing deposit, borrow, and liquidation transactions.
- **Wallet Features Calculation**: Computes important wallet features like deposit/borrow ratio, liquidation rates, and active days.
- **Scoring Model**: Uses a weighted scoring system based on several wallet behaviors.
- **Output**: Generates a list of top 1000 wallets with their credit scores and a summary report on top and bottom wallets.

## Files
- **data/**: Contains the raw CSV data files:
  - `deposits.csv`
  - `borrows.csv`
  - `liquidations.csv`
- **outputs/**: Stores the resulting output files:
  - `wallet_scores.csv`: Contains the credit scores of wallets.
  - `wallet_analysis.txt`: A text file with detailed analysis of the top and bottom wallets.

## Requirements
- Python 3.x
- pandas
- numpy
- scikit-learn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MIDHUNMAMEN/Assesment-_zeru-credit-score.git
   cd credit-scoring
