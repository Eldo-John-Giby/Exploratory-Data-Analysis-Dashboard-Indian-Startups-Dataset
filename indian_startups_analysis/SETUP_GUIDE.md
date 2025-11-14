# Project Setup & Execution Guide

## 🚀 Quick Start Guide

### Option 1: Use Your Own Dataset

1. Place your dataset in `data/` folder as `indian_startups_funding.csv`
2. Ensure it has these columns (or similar):
   - startup_name / company_name
   - industry / sector / vertical
   - city
   - state
   - funding_amount / amount (in any currency)
   - funding_round / round / stage
   - investors / investor
   - date / funding_date

3. Run the analysis:
```bash
cd src
python main.py
```

### Option 2: Generate Sample Dataset

If you don't have a dataset, generate a sample one:

```bash
cd src
python generate_sample_data.py
python main.py
```

---

## 📦 Installation Steps (Detailed)

### 1. System Requirements

- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB for project + dependencies
- **OS**: Windows, macOS, or Linux

### 2. Clone or Download Project

```bash
git clone <repository-url>
cd indian_startups_analysis
```

Or download and extract the ZIP file.

### 3. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list
```

You should see:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- And others...

---

## 🎯 Execution Workflow

### Step 1: Prepare Data

**If using your own data:**
- Place CSV in `data/` folder
- Name it `indian_startups_funding.csv` (or update path in main.py)

**If generating sample data:**
```bash
cd src
python generate_sample_data.py
```

### Step 2: Run Complete Analysis

```bash
cd src
python main.py
```

**Expected execution time:** 2-5 minutes (depending on dataset size)

**What happens:**
1. ✅ Data loaded and cleaned
2. ✅ 9 visualizations generated
3. ✅ K-Means model trained
4. ✅ Cluster analysis completed
5. ✅ Results saved

### Step 3: Review Outputs

**Generated files:**
```
data/
├── cleaned_startup_data.csv      # Cleaned dataset
└── startup_clusters.csv          # Clustering results

visualizations/
├── funding_distribution.png
├── top_startups.png
├── industry_analysis.png
├── geographic_analysis.png
├── time_trends.png
├── funding_rounds.png
├── investor_analysis.png
├── correlation_heatmap.png
├── outlier_analysis.png
├── elbow_method.png
└── cluster_visualization.png
```

### Step 4: SQL Analysis (Optional)

1. **Install MySQL/PostgreSQL** (if not already installed)

2. **Create database:**
```sql
CREATE DATABASE indian_startups_db;
```

3. **Run setup script:**
```bash
mysql -u root -p indian_startups_db < sql/database_setup.sql
```

4. **Load data:**
```sql
LOAD DATA LOCAL INFILE 'data/cleaned_startup_data.csv'
INTO TABLE startup_funding
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

5. **Execute analysis queries:**
```bash
mysql -u root -p indian_startups_db < sql/analysis_queries.sql
```

### Step 5: Power BI Dashboard

1. **Open Power BI Desktop**

2. **Import cleaned data:**
   - Get Data → Text/CSV
   - Select `data/cleaned_startup_data.csv`
   - Transform Data (Power Query)

3. **Import cluster data:**
   - Get Data → Text/CSV
   - Select `data/startup_clusters.csv`

4. **Follow instructions:**
   - Open `power_bi/dashboard_instructions.md`
   - Follow step-by-step guide
   - Create 4 dashboard pages

5. **Publish:**
   - File → Publish → Power BI
   - Share with stakeholders

---

## 🔧 Troubleshooting

### Issue 1: Module not found

**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
pip install pandas
# Or reinstall all
pip install -r requirements.txt
```

### Issue 2: Data file not found

**Error:** `FileNotFoundError: data/indian_startups_funding.csv`

**Solution:**
- Ensure data file exists in `data/` folder
- Check filename spelling
- Or generate sample data:
```bash
python src/generate_sample_data.py
```

### Issue 3: Matplotlib display issues

**Error:** Charts not showing or saving errors

**Solution:**
```bash
# Install backend
pip install --upgrade matplotlib

# For Linux, might need:
sudo apt-get install python3-tk
```

### Issue 4: Memory errors with large datasets

**Error:** `MemoryError` or system slowdown

**Solution:**
- Reduce dataset size (sample first N rows)
- Increase system RAM
- Process in chunks:
```python
# In data_loader.py, modify load_data():
df = pd.read_csv(filepath, nrows=10000)  # Limit rows
```

### Issue 5: SQL connection errors

**Error:** `Can't connect to MySQL server`

**Solution:**
1. Ensure MySQL/PostgreSQL is running
2. Check credentials in connection string
3. Verify port (default: 3306 for MySQL, 5432 for PostgreSQL)

### Issue 6: Power BI data not loading

**Error:** Data doesn't appear in Power BI

**Solution:**
1. Check file permissions
2. Ensure CSV is properly formatted (UTF-8)
3. Try importing smaller sample first
4. Check for special characters in paths

---

## 📊 Understanding Outputs

### Cleaned Data (cleaned_startup_data.csv)

**Columns:**
- startup_name: Cleaned and standardized
- industry: Categorized industries
- city, state: Geographic information
- funding_amount_usd: Numeric funding in USD
- funding_round: Standardized round names
- investors: Cleaned investor names
- date: Parsed dates
- year, month, quarter, month_name: Extracted time features

**Use for:**
- Power BI import
- Further analysis
- SQL database loading

### Cluster Results (startup_clusters.csv)

**Columns:**
- startup_name: Startup identifier
- cluster: Cluster number (0, 1, 2, ...)
- cluster_name: Descriptive name
- total_funding: Aggregated funding
- avg_funding_per_round: Average per round
- num_funding_rounds: Count of rounds
- years_active: Time span
- industry_first: Primary industry

**Use for:**
- Segmentation analysis
- Benchmarking
- Power BI cluster visuals

### Visualizations

**Purpose:** High-quality PNG files for:
- Reports and presentations
- Documentation
- Blog posts / articles
- Portfolio showcases

**Resolution:** 300 DPI (print quality)

---

## 🎓 Learning Path

### For Beginners

1. **Start with:**
   - Run `generate_sample_data.py` to create data
   - Execute `main.py` to see full pipeline
   - Review generated visualizations

2. **Explore:**
   - Open `data_loader.py` to understand cleaning
   - Check `eda_analysis.py` for visualization code
   - Study `clustering_model.py` for ML concepts

3. **Practice:**
   - Modify visualizations (colors, titles)
   - Change clustering parameters
   - Add new analysis functions

### For Intermediate Users

1. **Customize:**
   - Add new features in data_loader
   - Create custom visualizations
   - Implement additional ML models

2. **Extend:**
   - Add time series forecasting
   - Implement recommendation engine
   - Build web dashboard with Streamlit

3. **Optimize:**
   - Improve SQL query performance
   - Optimize data processing
   - Add data validation layers

### For Advanced Users

1. **Productionize:**
   - Add CI/CD pipeline
   - Implement automated testing
   - Set up monitoring and logging

2. **Scale:**
   - Handle larger datasets (1M+ rows)
   - Distributed processing with Dask/Spark
   - Deploy ML models as APIs

3. **Innovate:**
   - Add NLP for startup descriptions
   - Implement graph neural networks for investor networks
   - Build predictive models for funding success

---

## 📚 Additional Resources

### Documentation
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

### Tutorials
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [DataCamp](https://www.datacamp.com/)

### Communities
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- [Reddit r/datascience](https://www.reddit.com/r/datascience/)
- [Power BI Community](https://community.powerbi.com/)

---

## 🔄 Version Control

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit: Complete startup analysis project"
```

### Making Changes
```bash
# Create feature branch
git checkout -b feature/new-analysis

# Make changes, then:
git add .
git commit -m "Add new analysis feature"

# Merge back
git checkout main
git merge feature/new-analysis
```

### Pushing to GitHub
```bash
git remote add origin https://github.com/yourusername/indian-startups-analysis.git
git branch -M main
git push -u origin main
```

---

## 📞 Support

If you encounter issues:

1. **Check documentation** in this file and README.md
2. **Review error messages** carefully
3. **Search Stack Overflow** for similar issues
4. **Open an issue** on GitHub with:
   - Error message
   - System details
   - Steps to reproduce

---

## ✅ Completion Checklist

Before considering the project complete:

- [ ] Data loaded successfully
- [ ] All cleaning steps executed
- [ ] 9 visualizations generated
- [ ] K-Means model trained
- [ ] Cluster analysis completed
- [ ] SQL queries tested (if using SQL)
- [ ] Power BI dashboard created (if using Power BI)
- [ ] README.md reviewed
- [ ] All files organized properly
- [ ] Code documented
- [ ] Results validated

---

**Last Updated:** 2025-01-14  
**Version:** 1.0.0
