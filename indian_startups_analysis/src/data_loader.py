"""
Indian Startups Funding Analysis - Data Loading and Cleaning Module
Author: Data Science Team
Date: 2025-01-14
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    """
    Handles data loading and initial preprocessing for startup funding dataset
    """
    
    def __init__(self, filepath):
        """
        Initialize DataLoader with file path
        
        Args:
            filepath (str): Path to the dataset file
        """
        self.filepath = filepath
        self.df = None
        
    def load_data(self):
        """
        Load data from CSV or Excel file
        
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath, encoding='utf-8')
            elif self.filepath.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(self.filepath)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")
            
            print(f"[OK] Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return self.df
        
        except Exception as e:
            print(f"[ERROR] Error loading data: {str(e)}")
            raise
    
    def standardize_columns(self):
        """
        Standardize column names to expected format
        """
        column_mapping = {}
        
        for col in self.df.columns:
            col_lower = col.lower().strip()
            
            if 'startup' in col_lower or 'company' in col_lower:
                if 'startup_name' not in column_mapping.values():
                    column_mapping[col] = 'startup_name'
            elif 'industry' in col_lower or 'sector' in col_lower or 'vertical' in col_lower:
                if 'industry' not in column_mapping.values():
                    column_mapping[col] = 'industry'
            elif 'city' in col_lower and 'location' not in col_lower:
                if 'city' not in column_mapping.values():
                    column_mapping[col] = 'city'
            elif 'state' in col_lower:
                if 'state' not in column_mapping.values():
                    column_mapping[col] = 'state'
            elif 'amount' in col_lower or ('funding' in col_lower and 'usd' in col_lower):
                if 'funding_amount_usd' not in column_mapping.values():
                    column_mapping[col] = 'funding_amount_usd'
            elif 'round' in col_lower or 'stage' in col_lower:
                if 'funding_round' not in column_mapping.values():
                    column_mapping[col] = 'funding_round'
            elif 'investor' in col_lower:
                if 'investors' not in column_mapping.values():
                    column_mapping[col] = 'investors'
            elif 'date' in col_lower:
                if 'date' not in column_mapping.values():
                    column_mapping[col] = 'date'
        
        if column_mapping:
            self.df.rename(columns=column_mapping, inplace=True)
            print(f"[OK] Columns standardized: {list(column_mapping.values())}")
        
        return self.df
    
    def clean_data(self):
        """
        Comprehensive data cleaning pipeline
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("\n" + "="*60)
        print("DATA CLEANING PIPELINE")
        print("="*60)
        
        initial_rows = len(self.df)
        
        # Handle missing values
        print("\n1. Handling Missing Values:")
        print(f"   Missing values before:\n{self.df.isnull().sum()}")
        
        # Fill or drop based on column importance
        if 'startup_name' in self.df.columns:
            self.df = self.df.dropna(subset=['startup_name'])
        
        if 'funding_amount_usd' in self.df.columns:
            self.df['funding_amount_usd'].fillna(0, inplace=True)
        
        if 'industry' in self.df.columns:
            self.df['industry'].fillna('Unknown', inplace=True)
        
        if 'city' in self.df.columns:
            self.df['city'].fillna('Unknown', inplace=True)
        
        if 'state' in self.df.columns:
            self.df['state'].fillna('Unknown', inplace=True)
        
        if 'investors' in self.df.columns:
            self.df['investors'].fillna('Undisclosed', inplace=True)
        
        if 'funding_round' in self.df.columns:
            self.df['funding_round'].fillna('Unknown', inplace=True)
        
        print(f"   [OK] Missing values handled")
        
        # Clean funding amount
        if 'funding_amount_usd' in self.df.columns:
            print("\n2. Cleaning Funding Amount:")
            # Check if already numeric
            if pd.api.types.is_numeric_dtype(self.df['funding_amount_usd']):
                print(f"   [OK] Funding amounts already numeric")
            else:
                self.df['funding_amount_usd'] = self.df['funding_amount_usd'].apply(self._clean_amount)
                print(f"   [OK] Funding amounts converted to numeric")
        
        # Parse dates
        if 'date' in self.df.columns:
            print("\n3. Parsing Dates:")
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            self.df = self.df.dropna(subset=['date'])
            
            self.df['year'] = self.df['date'].dt.year
            self.df['month'] = self.df['date'].dt.month
            self.df['quarter'] = self.df['date'].dt.quarter
            self.df['month_name'] = self.df['date'].dt.month_name()
            print(f"   [OK] Date features extracted")
        
        # Remove duplicates
        print("\n4. Removing Duplicates:")
        duplicates = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        print(f"   [OK] {duplicates} duplicate rows removed")
        
        # Clean text fields
        print("\n5. Cleaning Text Fields:")
        text_columns = ['startup_name', 'industry', 'city', 'state', 'funding_round']
        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.title()
        print(f"   [OK] Text fields standardized")
        
        final_rows = len(self.df)
        print(f"\n" + "="*60)
        print(f"CLEANING SUMMARY: {initial_rows} → {final_rows} rows ({initial_rows - final_rows} removed)")
        print("="*60 + "\n")
        
        return self.df
    
    def _clean_amount(self, amount):
        """
        Convert funding amount to numeric (USD)
        
        Args:
            amount: Raw amount value
            
        Returns:
            float: Cleaned numeric amount
        """
        if pd.isna(amount):
            return 0
        
        if isinstance(amount, (int, float)):
            return float(amount)
        
        amount_str = str(amount).strip().upper()
        
        # Remove currency symbols
        amount_str = amount_str.replace('$', '').replace('₹', '').replace(',', '')
        
        # Handle millions, billions, etc.
        multiplier = 1
        if 'B' in amount_str or 'BILLION' in amount_str:
            multiplier = 1_000_000_000
            amount_str = amount_str.replace('B', '').replace('BILLION', '')
        elif 'M' in amount_str or 'MILLION' in amount_str:
            multiplier = 1_000_000
            amount_str = amount_str.replace('M', '').replace('MILLION', '')
        elif 'K' in amount_str or 'THOUSAND' in amount_str:
            multiplier = 1_000
            amount_str = amount_str.replace('K', '').replace('THOUSAND', '')
        elif 'CR' in amount_str or 'CRORE' in amount_str:
            multiplier = 10_000_000  # 1 crore = 10 million
            amount_str = amount_str.replace('CR', '').replace('CRORE', '')
        elif 'L' in amount_str or 'LAKH' in amount_str:
            multiplier = 100_000  # 1 lakh = 100 thousand
            amount_str = amount_str.replace('L', '').replace('LAKH', '')
        
        try:
            return float(amount_str.strip()) * multiplier
        except:
            return 0
    
    def get_summary_statistics(self):
        """
        Generate summary statistics for the dataset
        
        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_records': len(self.df),
            'total_startups': self.df['startup_name'].nunique() if 'startup_name' in self.df.columns else 0,
            'total_funding_usd': self.df['funding_amount_usd'].sum() if 'funding_amount_usd' in self.df.columns else 0,
            'avg_funding_usd': self.df['funding_amount_usd'].mean() if 'funding_amount_usd' in self.df.columns else 0,
            'total_industries': self.df['industry'].nunique() if 'industry' in self.df.columns else 0,
            'total_cities': self.df['city'].nunique() if 'city' in self.df.columns else 0,
            'date_range': f"{self.df['date'].min()} to {self.df['date'].max()}" if 'date' in self.df.columns else 'N/A'
        }
        
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value:,.0f}" if isinstance(value, (int, float)) else f"{key.replace('_', ' ').title()}: {value}")
        print("="*60 + "\n")
        
        return summary
    
    def save_cleaned_data(self, output_path):
        """
        Save cleaned data to CSV
        
        Args:
            output_path (str): Output file path
        """
        self.df.to_csv(output_path, index=False)
        print(f"[OK] Cleaned data saved to: {output_path}")


if __name__ == "__main__":
    # Example usage
    print("Data Loader Module - Ready for Import")

