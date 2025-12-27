import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_results():
    input_path = "validation_pipeline/analysis_results.csv"
    output_image = "validation_pipeline/power_inflation_chart.png"
    
    print("-" * 50)
    print("🎨 STARTING VISUALIZATION")
    print("-" * 50)

    if not os.path.exists(input_path):
        print("❌ Analysis results not found.")
        return

    df = pd.read_csv(input_path)
    
    # calculate percentage gap for plotting
    # Gap is already in the CSV, but let's ensure it's correct
    df['Gap Pct'] = df['Gap'] * 100
    
    # Sort for better plotting
    df = df.sort_values(by='Gap Pct', ascending=False)
    
    # Setup Plot
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # Color palette: Green for Inflation, Red for Deflation
    colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in df['Gap Pct']]
    
    ax = sns.barplot(x='Partai', y='Gap Pct', data=df, palette=colors)
    
    # Labels
    plt.title('Inflation vs Deflation of Political Power (Shapley-Shubik Index)\n2024 Indonesia Parliament Simulation', fontsize=14, fontweight='bold')
    plt.ylabel('Power Gap (Percentage Points)', fontsize=12)
    plt.xlabel('Political Party', fontsize=12)
    plt.axhline(0, color='black', linewidth=1)
    
    # Add value labels
    for i, v in enumerate(df['Gap Pct']):
        ax.text(i, v + (0.1 if v > 0 else -0.3), f"{v:+.2f}%", 
                ha='center', fontweight='bold', color='black')
                
    # Annotations
    plt.text(0.02, 0.95, 'Overpowered (Inflated)', transform=ax.transAxes, color='#2ecc71', fontweight='bold')
    plt.text(0.02, 0.05, 'Underpowered (Deflated)', transform=ax.transAxes, color='#e74c3c', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_image, dpi=300)
    print(f"✅ Chart saved to: {output_image}")
    # plt.show() # Disabled for headless execution

if __name__ == "__main__":
    visualize_results()
