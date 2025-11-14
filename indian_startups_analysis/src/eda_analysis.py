"""
Indian Startups Funding Analysis - Exploratory Data Analysis Module
Author: Data Science Team
Date: 2025-01-14
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class StartupEDA:
    """
    Comprehensive Exploratory Data Analysis for Startup Funding Dataset
    """
    
    def __init__(self, dataframe):
        """
        Initialize EDA with cleaned dataframe
        
        Args:
            dataframe (pd.DataFrame): Cleaned startup funding data
        """
        self.df = dataframe
        self.figures = []
        
    def analyze_funding_distribution(self, save_path='../visualizations/funding_distribution.png'):
        """
        Analyze and visualize funding amount distribution
        """
        print("\n" + "="*60)
        print("FUNDING DISTRIBUTION ANALYSIS")
        print("="*60)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Histogram
        axes[0, 0].hist(self.df['funding_amount_usd'], bins=50, edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Funding Amount (USD)', fontsize=12)
        axes[0, 0].set_ylabel('Frequency', fontsize=12)
        axes[0, 0].set_title('Distribution of Funding Amounts', fontsize=14, fontweight='bold')
        axes[0, 0].ticklabel_format(style='plain', axis='x')
        
        # Log-scale histogram
        positive_funding = self.df[self.df['funding_amount_usd'] > 0]['funding_amount_usd']
        axes[0, 1].hist(np.log10(positive_funding), bins=50, edgecolor='black', alpha=0.7, color='coral')
        axes[0, 1].set_xlabel('Log10(Funding Amount)', fontsize=12)
        axes[0, 1].set_ylabel('Frequency', fontsize=12)
        axes[0, 1].set_title('Distribution of Funding Amounts (Log Scale)', fontsize=14, fontweight='bold')
        
        # Box plot
        axes[1, 0].boxplot(self.df['funding_amount_usd'], vert=True, patch_artist=True,
                          boxprops=dict(facecolor='lightblue', alpha=0.7))
        axes[1, 0].set_ylabel('Funding Amount (USD)', fontsize=12)
        axes[1, 0].set_title('Funding Amount Box Plot (Outlier Detection)', fontsize=14, fontweight='bold')
        axes[1, 0].ticklabel_format(style='plain', axis='y')
        
        # Statistics
        stats_text = f"""
        Statistical Summary:
        
        Mean: ${self.df['funding_amount_usd'].mean():,.0f}
        Median: ${self.df['funding_amount_usd'].median():,.0f}
        Std Dev: ${self.df['funding_amount_usd'].std():,.0f}
        Min: ${self.df['funding_amount_usd'].min():,.0f}
        Max: ${self.df['funding_amount_usd'].max():,.0f}
        
        Percentiles:
        25th: ${self.df['funding_amount_usd'].quantile(0.25):,.0f}
        50th: ${self.df['funding_amount_usd'].quantile(0.50):,.0f}
        75th: ${self.df['funding_amount_usd'].quantile(0.75):,.0f}
        95th: ${self.df['funding_amount_usd'].quantile(0.95):,.0f}
        """
        
        axes[1, 1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                       verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        axes[1, 1].axis('off')
        axes[1, 1].set_title('Funding Statistics', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Funding distribution analysis saved to {save_path}")
        self.figures.append(fig)
        
        return fig
    
    def analyze_top_startups(self, top_n=15, save_path='../visualizations/top_startups.png'):
        """
        Analyze and visualize top funded startups
        """
        print("\n" + "="*60)
        print(f"TOP {top_n} FUNDED STARTUPS")
        print("="*60)
        
        top_startups = self.df.groupby('startup_name')['funding_amount_usd'].sum().sort_values(ascending=False).head(top_n)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.barh(range(len(top_startups)), top_startups.values, color=plt.cm.viridis(np.linspace(0, 1, len(top_startups))))
        ax.set_yticks(range(len(top_startups)))
        ax.set_yticklabels(top_startups.index, fontsize=11)
        ax.set_xlabel('Total Funding (USD)', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Most Funded Startups', fontsize=16, fontweight='bold', pad=20)
        ax.invert_yaxis()
        
        # Add value labels
        for i, (idx, value) in enumerate(top_startups.items()):
            ax.text(value, i, f'  ${value/1e6:.1f}M', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Top startups analysis saved to {save_path}")
        
        print("\nTop 10 Startups by Funding:")
        for i, (name, amount) in enumerate(top_startups.head(10).items(), 1):
            print(f"  {i:2d}. {name[:40]:40s} ${amount/1e6:10.2f}M")
        
        self.figures.append(fig)
        return fig
    
    def analyze_industry_trends(self, top_n=12, save_path='../visualizations/industry_analysis.png'):
        """
        Analyze funding trends by industry
        """
        print("\n" + "="*60)
        print("INDUSTRY ANALYSIS")
        print("="*60)
        
        industry_funding = self.df.groupby('industry')['funding_amount_usd'].agg(['sum', 'count', 'mean']).sort_values('sum', ascending=False).head(top_n)
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        # Total funding by industry
        axes[0].barh(range(len(industry_funding)), industry_funding['sum'].values, 
                     color=plt.cm.plasma(np.linspace(0, 1, len(industry_funding))))
        axes[0].set_yticks(range(len(industry_funding)))
        axes[0].set_yticklabels(industry_funding.index, fontsize=10)
        axes[0].set_xlabel('Total Funding (USD)', fontsize=12, fontweight='bold')
        axes[0].set_title(f'Top {top_n} Industries by Total Funding', fontsize=14, fontweight='bold')
        axes[0].invert_yaxis()
        
        for i, value in enumerate(industry_funding['sum'].values):
            axes[0].text(value, i, f'  ${value/1e9:.2f}B' if value >= 1e9 else f'  ${value/1e6:.1f}M', 
                        va='center', fontsize=9)
        
        # Number of startups by industry
        axes[1].barh(range(len(industry_funding)), industry_funding['count'].values,
                     color=plt.cm.cividis(np.linspace(0, 1, len(industry_funding))))
        axes[1].set_yticks(range(len(industry_funding)))
        axes[1].set_yticklabels(industry_funding.index, fontsize=10)
        axes[1].set_xlabel('Number of Funding Rounds', fontsize=12, fontweight='bold')
        axes[1].set_title(f'Top {top_n} Industries by Number of Deals', fontsize=14, fontweight='bold')
        axes[1].invert_yaxis()
        
        for i, value in enumerate(industry_funding['count'].values):
            axes[1].text(value, i, f'  {int(value)}', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Industry analysis saved to {save_path}")
        
        print(f"\nTop {min(10, top_n)} Industries:")
        for i, (ind, row) in enumerate(industry_funding.head(10).iterrows(), 1):
            print(f"  {i:2d}. {ind[:35]:35s} ${row['sum']/1e9:.2f}B ({int(row['count'])} deals)")
        
        self.figures.append(fig)
        return fig
    
    def analyze_geographic_distribution(self, save_path='../visualizations/geographic_analysis.png'):
        """
        Analyze funding by geography (city and state)
        """
        print("\n" + "="*60)
        print("GEOGRAPHIC ANALYSIS")
        print("="*60)
        
        top_cities = self.df.groupby('city')['funding_amount_usd'].sum().sort_values(ascending=False).head(15)
        top_states = self.df.groupby('state')['funding_amount_usd'].sum().sort_values(ascending=False).head(15)
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        # Cities
        axes[0].bar(range(len(top_cities)), top_cities.values, color=plt.cm.Set3(np.linspace(0, 1, len(top_cities))))
        axes[0].set_xticks(range(len(top_cities)))
        axes[0].set_xticklabels(top_cities.index, rotation=45, ha='right', fontsize=10)
        axes[0].set_ylabel('Total Funding (USD)', fontsize=12, fontweight='bold')
        axes[0].set_title('Top 15 Cities by Funding', fontsize=14, fontweight='bold')
        axes[0].ticklabel_format(style='plain', axis='y')
        
        # States
        axes[1].bar(range(len(top_states)), top_states.values, color=plt.cm.Set2(np.linspace(0, 1, len(top_states))))
        axes[1].set_xticks(range(len(top_states)))
        axes[1].set_xticklabels(top_states.index, rotation=45, ha='right', fontsize=10)
        axes[1].set_ylabel('Total Funding (USD)', fontsize=12, fontweight='bold')
        axes[1].set_title('Top 15 States by Funding', fontsize=14, fontweight='bold')
        axes[1].ticklabel_format(style='plain', axis='y')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Geographic analysis saved to {save_path}")
        
        print("\nTop 10 Cities:")
        for i, (city, amount) in enumerate(top_cities.head(10).items(), 1):
            print(f"  {i:2d}. {city[:30]:30s} ${amount/1e9:.2f}B")
        
        self.figures.append(fig)
        return fig
    
    def analyze_time_trends(self, save_path='../visualizations/time_trends.png'):
        """
        Analyze funding trends over time
        """
        print("\n" + "="*60)
        print("TEMPORAL ANALYSIS")
        print("="*60)
        
        yearly_funding = self.df.groupby('year')['funding_amount_usd'].agg(['sum', 'count', 'mean']).reset_index()
        monthly_funding = self.df.groupby(['year', 'month'])['funding_amount_usd'].sum().reset_index()
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        
        # Yearly total funding
        axes[0, 0].plot(yearly_funding['year'], yearly_funding['sum'], marker='o', linewidth=2.5, markersize=8, color='darkblue')
        axes[0, 0].fill_between(yearly_funding['year'], yearly_funding['sum'], alpha=0.3)
        axes[0, 0].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Total Funding (USD)', fontsize=12, fontweight='bold')
        axes[0, 0].set_title('Year-over-Year Total Funding', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].ticklabel_format(style='plain', axis='y')
        
        # Yearly deal count
        axes[0, 1].bar(yearly_funding['year'], yearly_funding['count'], color='teal', alpha=0.7, edgecolor='black')
        axes[0, 1].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Number of Deals', fontsize=12, fontweight='bold')
        axes[0, 1].set_title('Year-over-Year Deal Count', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Average deal size
        axes[1, 0].plot(yearly_funding['year'], yearly_funding['mean'], marker='s', linewidth=2.5, 
                       markersize=8, color='darkred')
        axes[1, 0].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Average Funding (USD)', fontsize=12, fontweight='bold')
        axes[1, 0].set_title('Average Deal Size Over Time', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].ticklabel_format(style='plain', axis='y')
        
        # Monthly trend (recent years)
        recent_data = self.df[self.df['year'] >= self.df['year'].max() - 2]
        monthly_recent = recent_data.groupby(recent_data['date'].dt.to_period('M'))['funding_amount_usd'].sum()
        axes[1, 1].plot(range(len(monthly_recent)), monthly_recent.values, marker='o', linewidth=2, color='green')
        axes[1, 1].set_xlabel('Month (Recent 2 Years)', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Total Funding (USD)', fontsize=12, fontweight='bold')
        axes[1, 1].set_title('Monthly Funding Trend (Last 2 Years)', fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].ticklabel_format(style='plain', axis='y')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Time trends analysis saved to {save_path}")
        
        print("\nYearly Funding Summary:")
        for _, row in yearly_funding.iterrows():
            print(f"  {int(row['year'])}: ${row['sum']/1e9:.2f}B ({int(row['count'])} deals, avg: ${row['mean']/1e6:.1f}M)")
        
        self.figures.append(fig)
        return fig
    
    def analyze_funding_rounds(self, save_path='../visualizations/funding_rounds.png'):
        """
        Analyze funding by round type
        """
        print("\n" + "="*60)
        print("FUNDING ROUND ANALYSIS")
        print("="*60)
        
        round_analysis = self.df.groupby('funding_round')['funding_amount_usd'].agg(['sum', 'count', 'mean']).sort_values('sum', ascending=False)
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        # Pie chart - funding by round
        colors = plt.cm.Set3(np.linspace(0, 1, len(round_analysis.head(10))))
        wedges, texts, autotexts = axes[0].pie(round_analysis.head(10)['sum'], labels=round_analysis.head(10).index,
                                                autopct='%1.1f%%', startangle=90, colors=colors)
        axes[0].set_title('Funding Distribution by Round Type (Top 10)', fontsize=14, fontweight='bold')
        
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Bar chart - count by round
        axes[1].barh(range(len(round_analysis.head(12))), round_analysis.head(12)['count'].values,
                     color=plt.cm.viridis(np.linspace(0, 1, 12)))
        axes[1].set_yticks(range(len(round_analysis.head(12))))
        axes[1].set_yticklabels(round_analysis.head(12).index, fontsize=10)
        axes[1].set_xlabel('Number of Deals', fontsize=12, fontweight='bold')
        axes[1].set_title('Number of Deals by Round Type', fontsize=14, fontweight='bold')
        axes[1].invert_yaxis()
        
        for i, value in enumerate(round_analysis.head(12)['count'].values):
            axes[1].text(value, i, f'  {int(value)}', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Funding round analysis saved to {save_path}")
        
        print("\nTop Funding Rounds:")
        for i, (round_type, row) in enumerate(round_analysis.head(10).iterrows(), 1):
            print(f"  {i:2d}. {round_type[:25]:25s} ${row['sum']/1e9:.2f}B ({int(row['count'])} deals)")
        
        self.figures.append(fig)
        return fig
    
    def analyze_investors(self, top_n=20, save_path='../visualizations/investor_analysis.png'):
        """
        Analyze most active investors
        """
        print("\n" + "="*60)
        print("INVESTOR ANALYSIS")
        print("="*60)
        
        # Split investors if multiple are listed
        all_investors = []
        for investors_str in self.df['investors'].dropna():
            if isinstance(investors_str, str):
                investors_list = [inv.strip() for inv in investors_str.split(',')]
                all_investors.extend(investors_list)
        
        investor_series = pd.Series(all_investors)
        top_investors = investor_series.value_counts().head(top_n)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        bars = ax.barh(range(len(top_investors)), top_investors.values,
                       color=plt.cm.coolwarm(np.linspace(0, 1, len(top_investors))))
        ax.set_yticks(range(len(top_investors)))
        ax.set_yticklabels(top_investors.index, fontsize=10)
        ax.set_xlabel('Number of Investments', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Most Active Investors', fontsize=16, fontweight='bold', pad=20)
        ax.invert_yaxis()
        
        for i, value in enumerate(top_investors.values):
            ax.text(value, i, f'  {int(value)}', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Investor analysis saved to {save_path}")
        
        print(f"\nTop {min(15, top_n)} Most Active Investors:")
        for i, (investor, count) in enumerate(top_investors.head(15).items(), 1):
            print(f"  {i:2d}. {investor[:50]:50s} {int(count):4d} investments")
        
        self.figures.append(fig)
        return fig
    
    def create_correlation_heatmap(self, save_path='../visualizations/correlation_heatmap.png'):
        """
        Create correlation heatmap for numerical features
        """
        print("\n" + "="*60)
        print("CORRELATION ANALYSIS")
        print("="*60)
        
        # Create additional numerical features for correlation
        correlation_df = self.df.copy()
        correlation_df['funding_log'] = np.log10(correlation_df['funding_amount_usd'] + 1)
        
        # Select numerical columns
        numerical_cols = ['funding_amount_usd', 'funding_log', 'year', 'month', 'quarter']
        corr_data = correlation_df[numerical_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_title('Correlation Matrix - Numerical Features', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Correlation heatmap saved to {save_path}")
        
        self.figures.append(fig)
        return fig
    
    def detect_outliers(self, save_path='../visualizations/outlier_analysis.png'):
        """
        Detect and visualize outliers in funding amounts
        """
        print("\n" + "="*60)
        print("OUTLIER DETECTION")
        print("="*60)
        
        Q1 = self.df['funding_amount_usd'].quantile(0.25)
        Q3 = self.df['funding_amount_usd'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df['funding_amount_usd'] < lower_bound) | 
                          (self.df['funding_amount_usd'] > upper_bound)]
        
        print(f"Total outliers detected: {len(outliers)} ({len(outliers)/len(self.df)*100:.1f}%)")
        print(f"Lower bound: ${lower_bound:,.0f}")
        print(f"Upper bound: ${upper_bound:,.0f}")
        
        if len(outliers) > 0:
            print("\nTop 10 Outliers (Highest Funding):")
            top_outliers = outliers.nlargest(10, 'funding_amount_usd')[['startup_name', 'funding_amount_usd', 'industry', 'year']]
            for i, row in top_outliers.iterrows():
                print(f"  {row['startup_name'][:35]:35s} ${row['funding_amount_usd']/1e9:.2f}B ({row['industry']}, {int(row['year'])})")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Scatter plot
        axes[0].scatter(range(len(self.df)), self.df['funding_amount_usd'], alpha=0.5, s=20)
        axes[0].axhline(y=upper_bound, color='r', linestyle='--', label=f'Upper Bound: ${upper_bound/1e6:.1f}M')
        axes[0].axhline(y=Q3, color='orange', linestyle='--', label=f'Q3: ${Q3/1e6:.1f}M')
        axes[0].axhline(y=Q1, color='green', linestyle='--', label=f'Q1: ${Q1/1e6:.1f}M')
        axes[0].set_xlabel('Index', fontsize=12)
        axes[0].set_ylabel('Funding Amount (USD)', fontsize=12)
        axes[0].set_title('Outlier Detection - Scatter Plot', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].ticklabel_format(style='plain', axis='y')
        
        # Box plot by year
        years = sorted(self.df['year'].unique())[-5:]  # Last 5 years
        data_by_year = [self.df[self.df['year'] == year]['funding_amount_usd'].values for year in years]
        
        bp = axes[1].boxplot(data_by_year, labels=years, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
            patch.set_alpha(0.7)
        axes[1].set_xlabel('Year', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Funding Amount (USD)', fontsize=12, fontweight='bold')
        axes[1].set_title('Funding Distribution by Year (Last 5 Years)', fontsize=14, fontweight='bold')
        axes[1].ticklabel_format(style='plain', axis='y')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Outlier analysis saved to {save_path}")
        
        self.figures.append(fig)
        return outliers
    
    def generate_comprehensive_report(self):
        """
        Generate all analyses and visualizations
        """
        print("\n" + "="*70)
        print(" "*15 + "COMPREHENSIVE EDA REPORT")
        print("="*70)
        
        self.analyze_funding_distribution()
        self.analyze_top_startups()
        self.analyze_industry_trends()
        self.analyze_geographic_distribution()
        self.analyze_time_trends()
        self.analyze_funding_rounds()
        self.analyze_investors()
        self.create_correlation_heatmap()
        self.detect_outliers()
        
        print("\n" + "="*70)
        print("[OK] COMPREHENSIVE EDA COMPLETED - All visualizations generated!")
        print("="*70 + "\n")
        
        return self.figures


if __name__ == "__main__":
    print("EDA Module - Ready for Import")

