import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# File paths
DEPOSIT_FILE = 'data/deposits.csv'
BORROW_FILE = 'data/borrows.csv'
LIQUIDATION_FILE = 'data/liquidations.csv'


deposits = pd.read_csv(DEPOSIT_FILE)
borrows = pd.read_csv(BORROW_FILE)
liquidations = pd.read_csv(LIQUIDATION_FILE)

deposits['action'] = 'deposit'
borrows['action'] = 'borrow'
liquidations['action'] = 'liquidation'

df = pd.concat([deposits, borrows, liquidations])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
df.dropna(subset=['timestamp'], inplace=True)

# Ensure 'amount' column is numeric to prevent TypeErrors
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df = df.fillna({'amount': 0})  # Replace NaN amounts with 0


group = df.groupby('account_id')

wallet_features = pd.DataFrame(index=group.groups.keys())

wallet_features['num_txns'] = group.size()
wallet_features['total_deposit'] = group.apply(lambda x: x[x['action'] == 'deposit']['amount'].sum())
wallet_features['total_borrow'] = group.apply(lambda x: x[x['action'] == 'borrow']['amount'].sum())
wallet_features['total_liquidation'] = group.apply(lambda x: x[x['action'] == 'liquidation']['amount'].sum())

wallet_features['deposit_count'] = group.apply(lambda x: (x['action'] == 'deposit').sum())
wallet_features['borrow_count'] = group.apply(lambda x: (x['action'] == 'borrow').sum())
wallet_features['liquidation_count'] = group.apply(lambda x: (x['action'] == 'liquidation').sum())

wallet_features['active_days'] = group['timestamp'].apply(lambda x: (x.max() - x.min()).days + 1)

wallet_features['deposit_borrow_ratio'] = wallet_features['total_deposit'] / (wallet_features['total_borrow'] + 1)
wallet_features['liquidation_rate'] = wallet_features['liquidation_count'] / (wallet_features['borrow_count'] + 1)

wallet_features = wallet_features.fillna(0)


scaler = MinMaxScaler()
scaled = scaler.fit_transform(wallet_features)

scaled_df = pd.DataFrame(scaled, columns=wallet_features.columns, index=wallet_features.index)

scaled_df['score'] = (
    0.3 * scaled_df['deposit_borrow_ratio'] +
    0.2 * scaled_df['active_days'] +
    0.3 * (1 - scaled_df['liquidation_rate']) +
    0.2 * scaled_df['deposit_count']
)

scaled_df['score'] = (scaled_df['score'] * 100).round(2)

top_1000 = scaled_df.sort_values('score', ascending=False).head(1000)
top_1000[['score']].to_csv('outputs/wallet_scores.csv')


def summarize_wallet(wallet_id):
    w = wallet_features.loc[wallet_id]
    return f"""
Wallet: {wallet_id}
Total Deposit: {w['total_deposit']:.2f}
Total Borrow: {w['total_borrow']:.2f}
Liquidations: {w['liquidation_count']}
Deposit Count: {w['deposit_count']}
Borrow Count: {w['borrow_count']}
Active Days: {w['active_days']}
Deposit/Borrow Ratio: {w['deposit_borrow_ratio']:.2f}
Liquidation Rate: {w['liquidation_rate']:.2f}
"""

with open('outputs/wallet_analysis.txt', 'w') as f:
    f.write("Top 5 High-Scoring Wallets:\n\n")
    for wallet in top_1000.head(5).index:
        f.write(summarize_wallet(wallet) + '\n')

    f.write("\nBottom 5 Low-Scoring Wallets:\n\n")
    for wallet in scaled_df.sort_values('score').head(5).index:
        f.write(summarize_wallet(wallet) + '\n')



