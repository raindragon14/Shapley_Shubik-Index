import os
import subprocess
import time

def run_step(script_name, description):
    print(f"\n▶️  STEP: {description}")
    start_time = time.time()
    result = subprocess.run(["python", script_name], capture_output=False)
    duration = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ {script_name} completed in {duration:.2f}s")
        return True
    else:
        print(f"❌ {script_name} failed!")
        return False

def main():
    print("="*60)
    print("🚀 EMPIRICAL VALIDATION PIPELINE: SHAPLEY-SHUBIK INDEX")
    print("="*60)
    
    steps = [
        ("validation_pipeline/01_scrape_data.py", "Scraping Data from Wikipedia"),
        ("validation_pipeline/02_process_data.py", "Cleaning and Validating Data"),
        ("validation_pipeline/03_analyze_power.py", "Calculating Power Indices"),
        ("validation_pipeline/04_visualize.py", "Generating Visualizations")
    ]
    
    for script, desc in steps:
        if not run_step(script, desc):
            print("\n⛔ Pipeline aborted due to error.")
            return

    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print("📂 Artifacts generated:")
    print("   - validation_pipeline/raw_data.csv")
    print("   - validation_pipeline/clean_data.csv")
    print("   - validation_pipeline/analysis_results.csv")
    print("   - validation_pipeline/power_inflation_chart.png")

if __name__ == "__main__":
    main()
