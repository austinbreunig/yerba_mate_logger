import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data.csv"

def update_charts():
    if not DATA_PATH.exists():
        return
    
    df = pd.read_csv(DATA_PATH)

    # Chart 1: Rating over time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plt.figure()
    sns.lineplot(x='timestamp', y='rating', data=df, marker='o')
    plt.title('Yerba Mate Ratings Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('rating_over_time.png')

    # Chart 2: Average rating by type
    plt.figure()
    sns.barplot(x='type', y='rating', data=df, estimator='mean', ci=None)
    plt.title('Average Rating by Type')
    plt.tight_layout()
    plt.savefig('rating_by_type.png')

    # Chart 3: Brand frequency
    plt.figure()
    sns.countplot(x='brand', data=df)
    plt.title('Tastings by Brand')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('tastings_by_brand.png')

