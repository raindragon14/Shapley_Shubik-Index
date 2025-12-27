import itertools
import math
import sys
from typing import List, Dict, Tuple

class WeightedVotingGame:
    def __init__(self, quota: int, weights: Dict[str, int]):
        """
        Initialize the Weighted Voting Game.
        
        Args:
            quota (int): The threshold required to win.
            weights (Dict[str, int]): A dictionary mapping player names to their weights (seats).
        """
        self.quota = quota
        self.weights = weights
        self.players = list(weights.keys())
        self.n = len(self.players)
        self.total_seats = sum(weights.values())

    def calculate_shapley_shubik(self):
        """
        Calculates the Shapley-Shubik power index for each player.
        
        Returns:
            pd.DataFrame: A DataFrame containing seats, % seats, pivot counts, and power indices.
        """
        import pandas as pd # Import here to avoid dependency if just using the class structure
        
        pivot_counts = {player: 0 for player in self.players}
        permutations = itertools.permutations(self.players)
        factorial_n = math.factorial(self.n)
        
        # Iterate through all possible orderings (permutations)
        for ordering in permutations:
            current_sum = 0
            for player in ordering:
                weight = self.weights[player]
                # Check if adding this player makes the coalition win (reach >= quota)
                if current_sum < self.quota and (current_sum + weight) >= self.quota:
                    pivot_counts[player] += 1
                    break # Found the pivot for this sequence, move to next
                current_sum += weight
                
        # Calculate indices
        results = []
        for player in self.players:
            seats = self.weights[player]
            count = pivot_counts[player]
            power_index = count / factorial_n
            seat_share = seats / self.total_seats
            
            results.append({
                "Partai": player,
                "Kursi": seats,
                "Seat Share": seat_share,
                "Pivot Count": count,
                "Shapley Index": power_index
            })
            
        return pd.DataFrame(results)

def main():
    try:
        import pandas as pd
    except ImportError:
        print("Error: This script requires pandas. Please run: pip install pandas")
        sys.exit(1)

    print("🏛️  ANALISIS KEKUATAN POLITIK: INDEKS SHAPLEY-SHUBIK 🏛️")
    print("-" * 60)
    
    # --- KONFIGURASI STUDI KASUS ---
    # Ubah data ini untuk simulasi kasus lain
    
    # Kasus: Paradoks 4 Partai
    quota = 51
    seats = {
        "Partai A": 45,
        "Partai B": 25,
        "Partai C": 20,
        "Partai D": 10
    }
    
    print(f"Total Kursi: {sum(seats.values())}")
    print(f"Quota Menang: {quota}")
    print(f"Pemain: {', '.join(seats.keys())}")
    print("-" * 60)
    print("Menghitung permutasi dan mencari pivot... (mohon tunggu)")
    
    game = WeightedVotingGame(quota, seats)
    df = game.calculate_shapley_shubik()
    
    print("\n📊 HASIL ANALISIS:")
    # Format for display
    display_df = df.copy()
    display_df['% Kursi'] = display_df['Seat Share'].apply(lambda x: f"{x:.2%}")
    display_df['Shapley Index'] = display_df['Shapley Index'].apply(lambda x: f"{x:.2%}")
    display_df['Gap'] = (df['Shapley Index'] - df['Seat Share'])
    display_df['Power/Seat Gap'] = display_df['Gap'].apply(lambda x: f"{x:.2%}")
    
    print(display_df[['Partai', 'Kursi', '% Kursi', 'Pivot Count', 'Shapley Index', 'Power/Seat Gap']].to_string(index=False))
    print("-" * 60)
    
    # Highlight Key Insight
    kingmakers = display_df[display_df['Gap'] > 0.001]
    if not kingmakers.empty:
        print("\n🏆 KINGMAKER DETECTED (Inflasi Kekuatan):")
        for _, row in kingmakers.iterrows():
            print(f"- {row['Partai']}: Kursi {row['% Kursi']} -> Kekuatan {row['Shapley Index']}")

if __name__ == "__main__":
    main()
