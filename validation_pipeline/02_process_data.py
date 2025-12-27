import pandas as pd
import os

def process_data():
    input_path = "validation_pipeline/raw_data.csv"
    output_path = "validation_pipeline/clean_data.csv"
    
    print("-" * 50)
    print("🧹 STARTING DATA CLEANING")
    print("-" * 50)

    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    
    # Validation Rules
    # 1. Total seats check
    total_seats = df['Kursi'].sum()
    print(f"📊 Total Seats Detected: {total_seats}")
    
    # KPU 2024 Total should be 580
    if total_seats != 580:
        print(f"⚠️  Warning: Total seats {total_seats} != 580.")
    else:
        print("✅ Total seats validated (580).")

    # 2. Sort by Seats descending
    df = df.sort_values(by='Kursi', ascending=False)
    
    # 3. Calculate Seat Share %
    df['Seat Share'] = df['Kursi'] / total_seats
    
    # Save
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved ({len(df)} parties) to: {output_path}")
    print(df[['Partai', 'Kursi', 'Seat Share']])

if __name__ == "__main__":
    process_data()
