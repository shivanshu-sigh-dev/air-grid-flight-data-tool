
import pandas as pd
import matplotlib.pyplot as plt

class FlightDataAnalyzer:
    """
    Analyze flight data from a CSV file and optionally display a chart.
    """
    def __init__(self, csv_path, show_chart=False):
        """
        Args:
            csv_path (str): Path to the CSV file containing flight data.
            show_chart (bool, optional): Whether to display the chart. Defaults to True.
        """
        self.csv_path = csv_path
        self.show_chart = show_chart
        self.df = pd.read_csv(csv_path)

    @staticmethod
    def parse_duration(d):
        """
        Convert duration string (e.g., '18h 10m') to total minutes.
        """
        parts = d.strip().split('h')
        hours = int(parts[0] or 0)
        minutes = 0
        if len(parts) > 1 and parts[1].strip():
            minutes = int(parts[1].replace('m','').strip())
        return hours*60 + minutes

    def analyze(self, w_price=0.6, w_dur=0.4, top_n=5):
        """
        Perform analysis and print best flights. Optionally show chart.

        Args:
            w_price (float): Weight for price normalization.
            w_dur (float): Weight for duration normalization.
            top_n (int): Number of top flights to display.
        """
        df = self.df.copy()
        df['duration_min'] = df['Duration'].apply(self.parse_duration)
        df['Price'] = df['Price (INR)'].astype(float)
        # Normalize to [0,1]
        df['price_norm'] = (df['Price'] - df['Price'].min()) / (df['Price'].max() - df['Price'].min())
        df['dur_norm']   = (df['duration_min'] - df['duration_min'].min()) / (df['duration_min'].max() - df['duration_min'].min())
        # Combined score (lower is better)
        df['score'] = w_price * df['price_norm'] + w_dur * df['dur_norm']
        best_flights = df.sort_values('score').head(top_n)
        
        if self.show_chart:
            plt.figure(figsize=(8,5))
            plt.scatter(df['duration_min'], df['Price'], c=df['score'], cmap='viridis')
            plt.xlabel('Duration (minutes)')
            plt.ylabel('Price (INR)')
            plt.colorbar(label='Combined score')
            plt.title('Price vs. Duration with Combined Score')
            plt.show()
        
        return best_flights[['Date','Airline','Price','duration_min','score']]