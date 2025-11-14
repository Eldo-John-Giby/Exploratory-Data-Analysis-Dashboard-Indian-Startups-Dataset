# Sample Dataset Generator for Indian Startups Funding Analysis

"""
This script generates a sample dataset for testing purposes.
If you have a real dataset, place it in the data/ folder and skip this script.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_RECORDS = 5000

# Sample data
STARTUP_NAMES = [
    "PayTech Solutions", "EduLearn", "HealthCare Plus", "FoodDelivery Express", 
    "FinanceApp", "TravelBuddy", "ShopEasy", "RideShare India", "AgriTech Innovations",
    "CloudServe", "AI Analytics", "GameZone", "MusicStream", "FitTrack", "HomeServices",
    "LegalTech", "PropertyFinder", "JobPortal Pro", "SocialConnect", "MediaHub",
    "EnergyEfficient", "WasteManagement Co", "FashionForward", "BeautyBox", "PetCare",
    "SportsFit", "EventPlanner", "WeddingBells", "AutoParts Direct", "ElectroMart",
    "FurnitureWorld", "BookMyService", "QuickGrocery", "PharmEasy Online", "DoctorConnect",
    "LabTest Now", "Insurance Plus", "LoanSimple", "InvestSmart", "CryptoTrade India",
    "BlockchainHub", "IoT Solutions", "RoboticsTech", "DroneDelivery", "SpaceTech Ventures",
    "BioTech Labs", "NanoTech India", "CleanEnergy Co", "SolarPower Solutions", "WindEnergy Tech",
    "WaterPurify", "AirQuality Monitor", "RecycleIt", "GreenBuild", "OrganicFarms",
    "VerticalGardens", "SmartCity Solutions", "TrafficManagement", "ParkingFinder", "EVCharging Network",
    "BatteryTech", "ChipManufacture", "SemiconductorHub", "DisplayTech", "CameraLens Co",
    "AudioTech", "SmartWatch India", "WearableTech", "ARGlasses", "VR Gaming",
    "Metaverse India", "NFT Marketplace", "DigitalArt Platform", "ContentCreators Hub", "Influencer Network",
    "AdTech Solutions", "MarketingAI", "SalesForce India", "CRM Platform", "HR Tech Solutions",
    "PayrollEasy", "RecruitmentAI", "TrainingHub", "SkillDevelopment", "CodingBootcamp",
    "DataScience Academy", "AI Research Lab", "ML Platform", "DeepLearning India", "NLP Solutions",
    "ComputerVision Co", "SpeechTech", "TranslationAI", "ChatbotBuilder", "VirtualAssistant India",
    "CloudStorage Pro", "DataBackup Solutions", "CyberSecurity India", "Firewall Tech", "Antivirus Plus",
    "IdentityVerification", "BiometricAuth", "PasswordManager", "SecureComm", "EncryptionTech",
    "PrivacyGuard", "AntiPhishing Co", "FraudDetection AI", "RiskAnalysis Platform", "ComplianceTech",
] * 60  # Duplicate to have enough names

INDUSTRIES = [
    "Fintech", "E-commerce", "Healthtech", "Edtech", "Foodtech",
    "Enterprise Software", "Consumer Services", "Logistics", "Travel & Hospitality", "Real Estate",
    "Media & Entertainment", "Gaming", "Fashion & Lifestyle", "Agritech", "CleanTech",
    "Automotive", "Hardware", "IoT", "AI/ML", "Blockchain",
    "Biotechnology", "Renewable Energy", "Analytics", "Marketing Tech", "HR Tech",
    "Cybersecurity", "Cloud Services", "SaaS", "Mobile Apps", "Social Media"
]

CITIES = [
    "Bangalore", "Mumbai", "Delhi", "Gurgaon", "Hyderabad",
    "Pune", "Chennai", "Noida", "Kolkata", "Ahmedabad",
    "Jaipur", "Surat", "Lucknow", "Chandigarh", "Kochi",
    "Indore", "Nagpur", "Bhopal", "Visakhapatnam", "Coimbatore"
]

STATES = {
    "Bangalore": "Karnataka", "Mumbai": "Maharashtra", "Delhi": "Delhi", 
    "Gurgaon": "Haryana", "Hyderabad": "Telangana", "Pune": "Maharashtra",
    "Chennai": "Tamil Nadu", "Noida": "Uttar Pradesh", "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat", "Jaipur": "Rajasthan", "Surat": "Gujarat",
    "Lucknow": "Uttar Pradesh", "Chandigarh": "Chandigarh", "Kochi": "Kerala",
    "Indore": "Madhya Pradesh", "Nagpur": "Maharashtra", "Bhopal": "Madhya Pradesh",
    "Visakhapatnam": "Andhra Pradesh", "Coimbatore": "Tamil Nadu"
}

FUNDING_ROUNDS = [
    "Seed", "Angel", "Pre-Series A", "Series A", "Series B", 
    "Series C", "Series D", "Series E", "Bridge Round", "Debt Financing",
    "Private Equity", "Growth Stage"
]

INVESTORS = [
    "Sequoia Capital", "Accel Partners", "Tiger Global", "SoftBank Vision Fund",
    "Nexus Venture Partners", "Matrix Partners", "Lightspeed Venture Partners",
    "Kalaari Capital", "Blume Ventures", "Chiratae Ventures",
    "SAIF Partners", "Elevation Capital", "Steadview Capital", "Falcon Edge",
    "Alpha Wave Incubation", "General Catalyst", "Insight Partners", "DST Global",
    "Naspers", "Tencent", "Alibaba", "Amazon", "Google Ventures",
    "Y Combinator", "500 Startups", "Techstars", "AngelList India"
]

def generate_dataset():
    """Generate sample startup funding dataset"""
    
    data = []
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for i in range(NUM_RECORDS):
        # Random startup (some startups will appear multiple times - multiple rounds)
        startup = random.choice(STARTUP_NAMES[:150])  # Limit to 150 unique startups
        industry = random.choice(INDUSTRIES)
        city = random.choice(CITIES)
        state = STATES[city]
        
        # Funding amount (log-normal distribution for realistic skew)
        base_amount = np.random.lognormal(mean=15, sigma=1.5)
        funding_amount = round(base_amount * 100000, 2)
        
        # Ensure some variety
        if random.random() < 0.7:  # 70% under $10M
            funding_amount = min(funding_amount, 10_000_000)
        elif random.random() < 0.2:  # 20% between $10M-$50M
            funding_amount = funding_amount * random.uniform(1, 5)
        else:  # 10% mega deals
            funding_amount = funding_amount * random.uniform(5, 50)
        
        # Round type
        funding_round = random.choice(FUNDING_ROUNDS)
        
        # Investors (1-3 investors)
        num_investors = random.randint(1, 3)
        investors = ", ".join(random.sample(INVESTORS, num_investors))
        
        # Date
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        funding_date = start_date + timedelta(days=random_days)
        
        data.append({
            'startup_name': startup,
            'industry': industry,
            'city': city,
            'state': state,
            'funding_amount_usd': funding_amount,
            'funding_round': funding_round,
            'investors': investors,
            'date': funding_date.strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(data)
    
    # Add some missing values to simulate real data
    missing_indices = random.sample(range(len(df)), k=int(len(df) * 0.02))
    for idx in missing_indices:
        col = random.choice(['industry', 'city', 'investors'])
        df.loc[idx, col] = np.nan
    
    # Add some duplicates
    duplicates = df.sample(n=50)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    print("Generating sample dataset...")
    df = generate_dataset()
    
    output_path = '../data/indian_startups_funding.csv'
    df.to_csv(output_path, index=False)
    
    print(f"[OK] Sample dataset generated: {len(df)} records")
    print(f"[OK] Saved to: {output_path}")
    print(f"\nDataset preview:")
    print(df.head(10))
    print(f"\nDataset info:")
    print(df.info())
    print(f"\nSummary statistics:")
    print(df.describe())

