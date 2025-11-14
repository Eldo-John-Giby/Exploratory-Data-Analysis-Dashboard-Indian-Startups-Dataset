"""
Indian Startups Funding Analysis - K-Means Clustering Model
Author: Data Science Team
Date: 2025-01-14
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class StartupClustering:
    """
    K-Means Clustering Analysis for Startup Segmentation
    """
    
    def __init__(self, dataframe):
        """
        Initialize clustering model
        
        Args:
            dataframe (pd.DataFrame): Cleaned startup funding data
        """
        self.df = dataframe
        self.scaler = StandardScaler()
        self.kmeans = None
        self.cluster_data = None
        self.optimal_k = None
        
    def prepare_features(self):
        """
        Prepare features for clustering
        
        Returns:
            pd.DataFrame: Feature dataframe
        """
        print("\n" + "="*60)
        print("FEATURE ENGINEERING FOR CLUSTERING")
        print("="*60)
        
        # Aggregate features per startup
        startup_features = self.df.groupby('startup_name').agg({
            'funding_amount_usd': ['sum', 'mean', 'count'],
            'year': ['min', 'max'],
            'industry': 'first',
            'city': 'first'
        }).reset_index()
        
        startup_features.columns = ['_'.join(col).strip('_') for col in startup_features.columns.values]
        startup_features.rename(columns={'startup_name': 'startup_name'}, inplace=True)
        
        # Create additional features
        startup_features['total_funding'] = startup_features['funding_amount_usd_sum']
        startup_features['avg_funding_per_round'] = startup_features['funding_amount_usd_mean']
        startup_features['num_funding_rounds'] = startup_features['funding_amount_usd_count']
        startup_features['years_active'] = startup_features['year_max'] - startup_features['year_min'] + 1
        startup_features['funding_per_year'] = startup_features['total_funding'] / startup_features['years_active']
        
        # Log transform for skewed features
        startup_features['log_total_funding'] = np.log10(startup_features['total_funding'] + 1)
        startup_features['log_avg_funding'] = np.log10(startup_features['avg_funding_per_round'] + 1)
        
        print(f"[OK] Features created for {len(startup_features)} startups")
        print(f"\nFeature columns:")
        for col in startup_features.columns:
            print(f"  - {col}")
        
        self.cluster_data = startup_features
        return startup_features
    
    def find_optimal_k(self, max_k=10, save_path='../visualizations/elbow_method.png'):
        """
        Use Elbow Method to find optimal number of clusters
        
        Args:
            max_k (int): Maximum number of clusters to test
            
        Returns:
            int: Optimal K value
        """
        print("\n" + "="*60)
        print("ELBOW METHOD - FINDING OPTIMAL K")
        print("="*60)
        
        # Select features for clustering
        feature_cols = ['log_total_funding', 'log_avg_funding', 'num_funding_rounds', 
                       'years_active', 'funding_per_year']
        X = self.cluster_data[feature_cols].fillna(0)
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Calculate inertia for different K values
        inertias = []
        K_range = range(2, max_k + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            print(f"  K={k}: Inertia={kmeans.inertia_:.2f}")
        
        # Plot elbow curve
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(K_range, inertias, 'bo-', linewidth=2, markersize=10)
        ax.set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=12, fontweight='bold')
        ax.set_title('Elbow Method for Optimal K', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        # Calculate rate of change
        rates = []
        for i in range(1, len(inertias)):
            rate = (inertias[i-1] - inertias[i]) / inertias[i-1] * 100
            rates.append(rate)
        
        # Find elbow (where rate of decrease slows down significantly)
        threshold = np.mean(rates) * 0.5
        for i, rate in enumerate(rates):
            if i > 0 and rate < threshold:
                self.optimal_k = i + 2
                break
        
        if self.optimal_k is None:
            self.optimal_k = 4  # Default
        
        ax.axvline(x=self.optimal_k, color='red', linestyle='--', linewidth=2, 
                  label=f'Suggested K={self.optimal_k}')
        ax.legend(fontsize=11)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n[OK] Optimal K identified: {self.optimal_k}")
        print(f"[OK] Elbow curve saved to {save_path}")
        
        return self.optimal_k
    
    def train_kmeans(self, n_clusters=None):
        """
        Train K-Means clustering model
        
        Args:
            n_clusters (int): Number of clusters (uses optimal_k if None)
            
        Returns:
            KMeans: Trained model
        """
        if n_clusters is None:
            n_clusters = self.optimal_k if self.optimal_k else 4
        
        print("\n" + "="*60)
        print(f"TRAINING K-MEANS MODEL (K={n_clusters})")
        print("="*60)
        
        # Select features
        feature_cols = ['log_total_funding', 'log_avg_funding', 'num_funding_rounds', 
                       'years_active', 'funding_per_year']
        X = self.cluster_data[feature_cols].fillna(0)
        
        # Normalize
        X_scaled = self.scaler.fit_transform(X)
        
        # Train K-Means
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_data['cluster'] = self.kmeans.fit_predict(X_scaled)
        
        print(f"[OK] K-Means model trained successfully")
        print(f"\nCluster Distribution:")
        cluster_counts = self.cluster_data['cluster'].value_counts().sort_index()
        for cluster, count in cluster_counts.items():
            print(f"  Cluster {cluster}: {count} startups ({count/len(self.cluster_data)*100:.1f}%)")
        
        return self.kmeans
    
    def analyze_clusters(self):
        """
        Analyze and interpret cluster characteristics
        
        Returns:
            pd.DataFrame: Cluster summary statistics
        """
        print("\n" + "="*60)
        print("CLUSTER ANALYSIS & INTERPRETATION")
        print("="*60)
        
        cluster_summary = self.cluster_data.groupby('cluster').agg({
            'total_funding': ['mean', 'median', 'sum'],
            'avg_funding_per_round': ['mean', 'median'],
            'num_funding_rounds': ['mean', 'median'],
            'years_active': ['mean', 'median'],
            'funding_per_year': ['mean', 'median']
        }).round(2)
        
        # Assign cluster names based on characteristics
        cluster_names = {}
        for cluster in sorted(self.cluster_data['cluster'].unique()):
            cluster_df = self.cluster_data[self.cluster_data['cluster'] == cluster]
            
            avg_funding = cluster_df['total_funding'].mean()
            avg_rounds = cluster_df['num_funding_rounds'].mean()
            
            if avg_funding > self.cluster_data['total_funding'].quantile(0.75):
                if avg_rounds > self.cluster_data['num_funding_rounds'].quantile(0.75):
                    cluster_names[cluster] = "High-Growth Unicorns"
                else:
                    cluster_names[cluster] = "Large Single-Round Players"
            elif avg_funding > self.cluster_data['total_funding'].quantile(0.50):
                cluster_names[cluster] = "Mid-Tier Growth Startups"
            elif avg_rounds > self.cluster_data['num_funding_rounds'].quantile(0.60):
                cluster_names[cluster] = "Frequent Small-Round Startups"
            else:
                cluster_names[cluster] = "Early-Stage Ventures"
        
        self.cluster_data['cluster_name'] = self.cluster_data['cluster'].map(cluster_names)
        
        print("\nCluster Profiles:")
        for cluster in sorted(self.cluster_data['cluster'].unique()):
            cluster_df = self.cluster_data[self.cluster_data['cluster'] == cluster]
            name = cluster_names[cluster]
            
            print(f"\n  Cluster {cluster}: {name}")
            print(f"    Size: {len(cluster_df)} startups")
            print(f"    Avg Total Funding: ${cluster_df['total_funding'].mean()/1e6:.2f}M")
            print(f"    Avg Rounds: {cluster_df['num_funding_rounds'].mean():.1f}")
            print(f"    Avg Years Active: {cluster_df['years_active'].mean():.1f}")
            print(f"    Top Industries: {', '.join(cluster_df['industry_first'].value_counts().head(3).index.tolist())}")
            
            # Show top 3 startups in cluster
            top_startups = cluster_df.nlargest(3, 'total_funding')
            print(f"    Top Startups:")
            for _, startup in top_startups.iterrows():
                print(f"      - {startup['startup_name'][:40]}: ${startup['total_funding']/1e6:.1f}M")
        
        return cluster_summary
    
    def visualize_clusters(self, save_path='../visualizations/cluster_visualization.png'):
        """
        Visualize clusters using PCA and various plots
        """
        print("\n" + "="*60)
        print("CLUSTER VISUALIZATION")
        print("="*60)
        
        # Select features
        feature_cols = ['log_total_funding', 'log_avg_funding', 'num_funding_rounds', 
                       'years_active', 'funding_per_year']
        X = self.cluster_data[feature_cols].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Apply PCA for 2D visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        print(f"PCA Explained Variance: {pca.explained_variance_ratio_[0]:.2%}, {pca.explained_variance_ratio_[1]:.2%}")
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        
        # 1. PCA Scatter Plot
        scatter = axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], 
                                     c=self.cluster_data['cluster'], 
                                     cmap='viridis', s=100, alpha=0.6, edgecolors='black')
        axes[0, 0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=12, fontweight='bold')
        axes[0, 0].set_title('Startup Clusters (PCA Projection)', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=axes[0, 0], label='Cluster')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Cluster sizes
        cluster_counts = self.cluster_data['cluster'].value_counts().sort_index()
        colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_counts)))
        axes[0, 1].bar(cluster_counts.index, cluster_counts.values, color=colors, edgecolor='black', alpha=0.7)
        axes[0, 1].set_xlabel('Cluster', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Number of Startups', fontsize=12, fontweight='bold')
        axes[0, 1].set_title('Cluster Size Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        for i, v in enumerate(cluster_counts.values):
            axes[0, 1].text(cluster_counts.index[i], v, str(v), ha='center', va='bottom', fontweight='bold')
        
        # 3. Average funding by cluster
        avg_funding = self.cluster_data.groupby('cluster')['total_funding'].mean().sort_index()
        axes[1, 0].barh(avg_funding.index, avg_funding.values / 1e6, color=colors, edgecolor='black', alpha=0.7)
        axes[1, 0].set_ylabel('Cluster', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Average Total Funding (Million USD)', fontsize=12, fontweight='bold')
        axes[1, 0].set_title('Average Funding by Cluster', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        for i, v in enumerate(avg_funding.values):
            axes[1, 0].text(v / 1e6, i, f'  ${v/1e6:.1f}M', va='center', fontweight='bold')
        
        # 4. Feature importance heatmap
        cluster_features = self.cluster_data.groupby('cluster')[feature_cols].mean()
        sns.heatmap(cluster_features.T, annot=True, fmt='.2f', cmap='YlOrRd', 
                   ax=axes[1, 1], cbar_kws={'label': 'Feature Value'})
        axes[1, 1].set_xlabel('Cluster', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Features', fontsize=12, fontweight='bold')
        axes[1, 1].set_title('Cluster Feature Profiles', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Cluster visualization saved to {save_path}")
        
        return fig
    
    def save_cluster_results(self, output_path='../data/startup_clusters.csv'):
        """
        Save clustering results to CSV
        
        Args:
            output_path (str): Output file path
        """
        self.cluster_data.to_csv(output_path, index=False)
        print(f"\n[OK] Cluster results saved to {output_path}")
    
    def run_complete_clustering(self):
        """
        Execute complete clustering pipeline
        """
        print("\n" + "="*70)
        print(" "*20 + "K-MEANS CLUSTERING PIPELINE")
        print("="*70)
        
        self.prepare_features()
        self.find_optimal_k()
        self.train_kmeans()
        cluster_summary = self.analyze_clusters()
        self.visualize_clusters()
        self.save_cluster_results()
        
        print("\n" + "="*70)
        print("[OK] CLUSTERING ANALYSIS COMPLETED!")
        print("="*70 + "\n")
        
        return self.cluster_data


if __name__ == "__main__":
    print("Clustering Module - Ready for Import")

