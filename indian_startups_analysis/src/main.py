"""
Indian Startups Funding Analysis - Main Execution Script
Author: Data Science Team
Date: 2025-01-14

This script orchestrates the complete analysis pipeline:
1. Data Loading & Cleaning
2. Exploratory Data Analysis
3. K-Means Clustering
"""

import sys
import os
from data_loader import DataLoader
from eda_analysis import StartupEDA
from clustering_model import StartupClustering
import warnings
warnings.filterwarnings('ignore')

def main():
    """
    Main execution function for the complete analysis pipeline
    """
    
    print("\n" + "="*80)
    print(" "*20 + "INDIAN STARTUPS FUNDING ANALYSIS")
    print(" "*25 + "Complete Data Science Project")
    print("="*80 + "\n")
    
    # Configuration
    DATA_FILE = '../data/indian_startups_funding.csv'  # Update with actual file path
    CLEANED_DATA_FILE = '../data/cleaned_startup_data.csv'
    
    # Check if data file exists
    if not os.path.exists(DATA_FILE):
        print(f"⚠ Data file not found: {DATA_FILE}")
        print("\nPlease ensure your dataset is placed in the data/ folder with one of these names:")
        print("  - indian_startups_funding.csv")
        print("  - startup_funding.csv")
        print("  - startups.csv")
        print("\nOr update the DATA_FILE variable in this script with your file path.")
        
        # Look for any CSV file in data folder
        data_dir = '../data'
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if csv_files:
                print(f"\nFound CSV files in data folder:")
                for f in csv_files:
                    print(f"  - {f}")
                DATA_FILE = os.path.join(data_dir, csv_files[0])
                print(f"\nUsing: {DATA_FILE}")
            else:
                print("\n⚠ No CSV files found in data folder.")
                print("Exiting... Please add your dataset and run again.")
                return
        else:
            print("\n⚠ Data folder not found.")
            print("Exiting... Please create data/ folder and add your dataset.")
            return
    
    try:
        # ============================================================
        # STEP 1: DATA LOADING & CLEANING
        # ============================================================
        print("\n" + "="*80)
        print("STEP 1: DATA LOADING & CLEANING")
        print("="*80)
        
        loader = DataLoader(DATA_FILE)
        df = loader.load_data()
        df = loader.standardize_columns()
        df = loader.clean_data()
        summary = loader.get_summary_statistics()
        loader.save_cleaned_data(CLEANED_DATA_FILE)
        
        # ============================================================
        # STEP 2: EXPLORATORY DATA ANALYSIS
        # ============================================================
        print("\n" + "="*80)
        print("STEP 2: EXPLORATORY DATA ANALYSIS")
        print("="*80)
        
        eda = StartupEDA(df)
        eda.generate_comprehensive_report()
        
        # ============================================================
        # STEP 3: K-MEANS CLUSTERING
        # ============================================================
        print("\n" + "="*80)
        print("STEP 3: K-MEANS CLUSTERING")
        print("="*80)
        
        clustering = StartupClustering(df)
        cluster_results = clustering.run_complete_clustering()
        
        # ============================================================
        # COMPLETION
        # ============================================================
        print("\n" + "="*80)
        print(" "*25 + "ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print("\nOUTPUTS GENERATED:")
        print("\n  Data Files:")
        print(f"    [OK] {CLEANED_DATA_FILE}")
        print(f"    [OK] ../data/startup_clusters.csv")
        
        print("\n  Visualizations:")
        print("    [OK] ../visualizations/funding_distribution.png")
        print("    [OK] ../visualizations/top_startups.png")
        print("    [OK] ../visualizations/industry_analysis.png")
        print("    [OK] ../visualizations/geographic_analysis.png")
        print("    [OK] ../visualizations/time_trends.png")
        print("    [OK] ../visualizations/funding_rounds.png")
        print("    [OK] ../visualizations/investor_analysis.png")
        print("    [OK] ../visualizations/correlation_heatmap.png")
        print("    [OK] ../visualizations/outlier_analysis.png")
        print("    [OK] ../visualizations/elbow_method.png")
        print("    [OK] ../visualizations/cluster_visualization.png")
        
        print("\nKEY INSIGHTS:")
        print(f"    - Total Funding: ${summary['total_funding_usd']/1e9:.2f}B")
        print(f"    - Total Startups: {summary['total_startups']:,}")
        print(f"    - Average Funding: ${summary['avg_funding_usd']/1e6:.2f}M")
        print(f"    - Industries Covered: {summary['total_industries']}")
        print(f"    - Cities Covered: {summary['total_cities']}")
        print(f"    - Date Range: {summary['date_range']}")
        
        print("\nNEXT STEPS:")
        print("    1. Review generated visualizations in visualizations/ folder")
        print("    2. Import cleaned_startup_data.csv into Power BI")
        print("    3. Follow Power BI instructions in power_bi/dashboard_instructions.md")
        print("    4. Use startup_clusters.csv for cluster-based insights")
        print("    5. Execute SQL queries from sql/ folder on your database")
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nPlease check the error above and try again.")


if __name__ == "__main__":
    main()
