import pandas as pd
import sys
import os

# Add parent directory to path to import shapley.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Attempt to import the shared class first
try:
    from shapley import WeightedVotingGame
except ImportError:
    print("⚠️  Warning: Could not import shapley.py, using local fallback.")
    import itertools
    import math
    class WeightedVotingGame:
        def __init__(self, quota, weights):
            self.quota = quota
            self.weights = weights
            self.players = list(weights.keys())
            self.n = len(self.players)
            self.total_seats = sum(weights.values())

        def calculate_shapley_shubik(self):
            pivot_counts = {p: 0 for p in self.players}
            perms = itertools.permutations(self.players)
            fact_n = math.factorial(self.n)
            
            for p_list in perms:
                cum_sum = 0
                for player in p_list:
                    w = self.weights[player]
                    if cum_sum < self.quota and (cum_sum + w) >= self.quota:
                        pivot_counts[player] += 1
                        break
                    cum_sum += w
            
            res = []
            for p in self.players:
                seats = self.weights[p]
                total = self.total_seats
                res.append({
                    "Partai": p,
                    "Kursi": seats,
                    "Seat Share": seats/total,
                    "Shapley Index": pivot_counts[p] / fact_n
                })
            return pd.DataFrame(res)

def analyze_power():
    input_path = "validation_pipeline/clean_data.csv"
    output_path = "validation_pipeline/analysis_results.csv"
    
    print("-" * 50)
    print("🧠 STARTING SHAPLEY-SHUBIK ANALYSIS")
    print("-" * 50)

    if not os.path.exists(input_path):
        print("❌ Data file not found.")
        return

    df = pd.read_csv(input_path)
    
    # Setup Game
    total_seats = df['Kursi'].sum()
    quota = (total_seats // 2) + 1  # Simple Majority (50% + 1)
    
    # Prepare Dict
    weights = dict(zip(df['Partai'], df['Kursi']))
    
    # Run Algorithm
    print(f"🎯 Configuration: Total={total_seats}, Quota={quota}")
    print("⏳ Calculating... (n=8 is fast, n>10 is slow)")
    
    game = WeightedVotingGame(quota, weights)
    results_df = game.calculate_shapley_shubik()
    
    # Merge results (on Partai) 
    # results_df already has Seat Share and Shapley Index as floats
    final_df = results_df.copy()
    
    # Calculate Gaps
    final_df['Gap'] = final_df['Shapley Index'] - final_df['Seat Share']
    final_df['Inflation Status'] = final_df['Gap'].apply(
        lambda x: 'INFLATED' if x > 0.001 else ('DEFLATED' if x < -0.001 else 'NEUTRAL')
    )
    
    # Formatting for display
    display_df = final_df.copy()
    display_df['Shapley Index'] = display_df['Shapley Index'].apply(lambda x: f"{x:.2%}")
    display_df['Seat Share'] = display_df['Seat Share'].apply(lambda x: f"{x:.2%}")
    display_df['Gap'] = display_df['Gap'].apply(lambda x: f"{x:+.2%}")
    
    print("\n🏆 FINAL RESULTS:")
    print(display_df[['Partai', 'Kursi', 'Seat Share', 'Shapley Index', 'Gap', 'Inflation Status']].to_string(index=False))
    
    final_df.to_csv(output_path, index=False)
    print(f"\n✅ Results saved to: {output_path}")

if __name__ == "__main__":
    analyze_power()
