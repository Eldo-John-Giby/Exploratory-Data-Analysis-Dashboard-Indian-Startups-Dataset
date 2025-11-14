# Power BI Dashboard - Step-by-Step Instructions

## Indian Startups Funding Analysis Dashboard

### 📊 Dashboard Overview

This guide provides complete instructions to build a professional Power BI dashboard with 4 main pages:
1. **Overview** - Key metrics and high-level insights
2. **Sector Analysis** - Industry-wise funding breakdown
3. **Geographic Analysis** - Location-based insights
4. **Investor & Clustering Insights** - Investment patterns and ML clusters

---

## 🚀 PART 1: Data Import & Power Query Setup

### Step 1: Import Data into Power BI

1. **Open Power BI Desktop**
2. Click **Get Data** → **Text/CSV**
3. Navigate to `data/cleaned_startup_data.csv`
4. Click **Transform Data** to open Power Query Editor

### Step 2: Power Query Transformations

#### A. Data Type Verification
```
1. Verify these column data types:
   - startup_name: Text
   - industry: Text
   - city: Text
   - state: Text
   - funding_amount_usd: Decimal Number
   - funding_round: Text
   - investors: Text
   - date: Date
   - year: Whole Number
   - month: Whole Number
   - quarter: Whole Number
   - month_name: Text

2. If any types are incorrect:
   - Right-click column header → Change Type → Select appropriate type
```

#### B. Add Custom Columns

**Funding Category Column:**
```M
= Table.AddColumn(#"Changed Type", "funding_category", each 
    if [funding_amount_usd] >= 100000000 then "100M+"
    else if [funding_amount_usd] >= 50000000 then "50M-100M"
    else if [funding_amount_usd] >= 10000000 then "10M-50M"
    else if [funding_amount_usd] >= 1000000 then "1M-10M"
    else "Under 1M")
```

**Funding in Millions:**
```M
= Table.AddColumn(#"Added Funding Category", "funding_millions", each [funding_amount_usd] / 1000000)
```

**Funding in Billions:**
```M
= Table.AddColumn(#"Added Funding Millions", "funding_billions", each [funding_amount_usd] / 1000000000)
```

**Year-Quarter:**
```M
= Table.AddColumn(#"Added Funding Billions", "year_quarter", each Text.From([year]) & " Q" & Text.From([quarter]))
```

### Step 3: Import Cluster Data

1. Click **Get Data** → **Text/CSV**
2. Load `data/startup_clusters.csv`
3. In Power Query, verify columns:
   - startup_name: Text
   - cluster: Whole Number
   - cluster_name: Text
   - total_funding: Decimal
   - num_funding_rounds: Whole Number

### Step 4: Create Relationships

1. Close Power Query (Close & Apply)
2. Go to **Model View** (left sidebar)
3. Create relationship:
   - Drag `startup_name` from `cleaned_startup_data` to `startup_name` in `startup_clusters`
   - Cardinality: Many to One (*:1)
   - Cross filter direction: Single

---

## 📐 PART 2: Create DAX Measures

### Step 1: Create Measures Table

1. Click **Home** → **Enter Data**
2. Create empty table named `_Measures`
3. Delete default columns
4. Click **Close & Load**

### Step 2: Add DAX Measures

Right-click `_Measures` table → **New Measure**, then paste each formula:

#### Basic Metrics

```DAX
Total Funding = SUM(cleaned_startup_data[funding_amount_usd])
```

```DAX
Total Funding (B) = [Total Funding] / 1000000000
```

```DAX
Total Funding (M) = [Total Funding] / 1000000
```

```DAX
Average Funding = AVERAGE(cleaned_startup_data[funding_amount_usd])
```

```DAX
Average Funding (M) = [Average Funding] / 1000000
```

```DAX
Total Deals = COUNTROWS(cleaned_startup_data)
```

```DAX
Total Startups = DISTINCTCOUNT(cleaned_startup_data[startup_name])
```

```DAX
Total Industries = DISTINCTCOUNT(cleaned_startup_data[industry])
```

```DAX
Total Cities = DISTINCTCOUNT(cleaned_startup_data[city])
```

```DAX
Total Investors = 
VAR AllInvestors = 
    SELECTCOLUMNS(
        cleaned_startup_data,
        "Investor", cleaned_startup_data[investors]
    )
RETURN
    COUNTROWS(DISTINCT(AllInvestors))
```

#### Year-over-Year Metrics

```DAX
Previous Year Funding = 
CALCULATE(
    [Total Funding],
    DATEADD(cleaned_startup_data[date], -1, YEAR)
)
```

```DAX
YoY Growth % = 
VAR CurrentYear = [Total Funding]
VAR PreviousYear = [Previous Year Funding]
RETURN
    IF(
        NOT(ISBLANK(PreviousYear)),
        DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100,
        BLANK()
    )
```

```DAX
YoY Growth Indicator = 
IF(
    [YoY Growth %] > 0,
    "▲ " & FORMAT([YoY Growth %], "0.0") & "%",
    "▼ " & FORMAT(ABS([YoY Growth %]), "0.0") & "%"
)
```

#### Advanced Metrics

```DAX
Median Funding = 
MEDIAN(cleaned_startup_data[funding_amount_usd])
```

```DAX
Top 10 Startup Funding = 
CALCULATE(
    [Total Funding],
    TOPN(
        10,
        ALL(cleaned_startup_data[startup_name]),
        [Total Funding],
        DESC
    )
)
```

```DAX
Top 10 % of Total = 
DIVIDE([Top 10 Startup Funding], [Total Funding], 0) * 100
```

```DAX
Avg Deals Per Startup = 
DIVIDE([Total Deals], [Total Startups], 0)
```

```DAX
Funding Concentration = 
VAR Top20Pct = 
    CALCULATE(
        [Total Funding],
        TOPN(
            INT([Total Startups] * 0.2),
            ALL(cleaned_startup_data[startup_name]),
            [Total Funding],
            DESC
        )
    )
RETURN
    DIVIDE(Top20Pct, [Total Funding], 0) * 100
```

---

## 🎨 PART 3: Build Dashboard Pages

### PAGE 1: Overview Dashboard

#### Layout Setup
1. **Page Background**: Light gray (#F5F5F5)
2. **Add Title**: Text box "Indian Startups Funding Analysis" (Font: Segoe UI, 28pt, Bold)
3. **Add Subtitle**: "Comprehensive Investment Overview" (Font: 16pt, Gray)

#### Visuals to Add:

**Row 1 - KPI Cards (4 cards in a row):**

1. **Total Funding KPI**
   - Visual: Card
   - Field: `Total Funding (B)`
   - Format → Data label: "$0.00B"
   - Format → Category label: "Total Funding"
   - Background: White
   - Border: Light gray

2. **Total Startups KPI**
   - Visual: Card
   - Field: `Total Startups`
   - Format → Data label: "#,0"
   - Format → Category label: "Startups Funded"

3. **Total Deals KPI**
   - Visual: Card
   - Field: `Total Deals`
   - Format → Data label: "#,0"
   - Format → Category label: "Funding Rounds"

4. **Average Funding KPI**
   - Visual: Card
   - Field: `Average Funding (M)`
   - Format → Data label: "$0.0M"
   - Format → Category label: "Avg Deal Size"

**Row 2 - Main Charts:**

5. **Year-over-Year Funding Trend**
   - Visual: Line and Clustered Column Chart
   - X-axis: `year`
   - Column values: `Total Funding (B)`
   - Line values: `Total Deals`
   - Title: "Yearly Funding Trend"
   - Format → Data colors: Blue (#0078D4) for columns, Orange (#FF8C00) for line
   - Format → Y-axis → Display units: Billions

6. **Top 15 Industries by Funding**
   - Visual: Bar Chart
   - Y-axis: `industry` (Top 15)
   - X-axis: `Total Funding (M)`
   - Title: "Top Industries by Total Funding"
   - Format → Data colors: Gradient (light blue to dark blue)
   - Format → Data labels: On
   - Format → X-axis → Display units: Millions

**Row 3 - Distribution Charts:**

7. **Funding by Round Type**
   - Visual: Donut Chart
   - Legend: `funding_round`
   - Values: `Total Funding (M)`
   - Title: "Funding Distribution by Round"
   - Format → Detail labels → Label style: Category, percentage

8. **Geographic Distribution (Top 10 Cities)**
   - Visual: Treemap
   - Group: `city`
   - Values: `Total Funding (M)`
   - Title: "Top Cities by Funding"
   - Format → Data labels: Category and value

**Row 4 - Detail Table:**

9. **Recent Top Deals**
   - Visual: Table
   - Columns (in order):
     - `startup_name`
     - `industry`
     - `city`
     - `funding_millions` (formatted as "$0.0M")
     - `funding_round`
     - `year`
   - Title: "Top 20 Funding Deals"
   - Sort by: `funding_millions` (descending)
   - Format → Grid: On
   - Format → Style: Alternating rows

#### Add Slicers:

10. **Year Slicer**
    - Visual: Slicer
    - Field: `year`
    - Slicer settings → Style: Dropdown
    - Position: Top right

11. **Industry Slicer**
    - Visual: Slicer
    - Field: `industry`
    - Slicer settings → Style: Dropdown
    - Position: Below year slicer

---

### PAGE 2: Sector Analysis

#### Layout Setup
1. Page title: "Sector & Industry Analysis"
2. Background: White

#### Visuals:

1. **Industry Performance Matrix**
   - Visual: Matrix
   - Rows: `industry`
   - Values:
     - `Total Funding (M)`
     - `Total Deals`
     - `Total Startups`
     - `Average Funding (M)`
   - Format → Conditional formatting on Total Funding (gradient)

2. **Top 15 Sectors - Funding Amount**
   - Visual: Horizontal Bar Chart
   - Y-axis: `industry` (Top 15 by Total Funding)
   - X-axis: `Total Funding (B)`
   - Data labels: On
   - Color: Gradient from light to dark

3. **Top 15 Sectors - Deal Count**
   - Visual: Horizontal Bar Chart
   - Y-axis: `industry` (Top 15 by Total Deals)
   - X-axis: `Total Deals`
   - Data labels: On
   - Color: Different gradient (green theme)

4. **Sector Funding Over Time**
   - Visual: Line Chart
   - X-axis: `year`
   - Y-axis: `Total Funding (B)`
   - Legend: `industry` (filtered to top 8)
   - Format → Lines: Markers on

5. **Industry Funding Categories**
   - Visual: Stacked Column Chart
   - X-axis: `industry` (Top 10)
   - Y-axis: `Total Deals`
   - Legend: `funding_category`
   - Title: "Deal Size Distribution by Industry"

6. **Industry Metrics Cards**
   - Top Industry by Funding (Card with TOPN filter)
   - Fastest Growing Industry (Custom DAX measure)

#### Slicers:
- Year range slicer
- Funding round filter

---

### PAGE 3: Geographic Analysis

#### Layout Setup
1. Page title: "Geographic Distribution & Hotspots"
2. Background: Light blue tint

#### Visuals:

1. **India Map Visualization**
   - Visual: Map (or Filled Map if states are properly named)
   - Location: `state`
   - Size: `Total Funding (M)`
   - Color saturation: `Total Startups`
   - Title: "Funding Heatmap by State"

2. **Top 20 Cities - Total Funding**
   - Visual: Bar Chart
   - Y-axis: `city` (Top 20)
   - X-axis: `Total Funding (M)`
   - Sort: Descending
   - Data labels: On

3. **Top 20 Cities - Startup Count**
   - Visual: Bar Chart
   - Y-axis: `city` (Top 20)
   - X-axis: `Total Startups`
   - Color: Different from above
   - Data labels: On

4. **State-wise Distribution**
   - Visual: Treemap
   - Group: `state`
   - Values: `Total Funding (B)`
   - Title: "State-wise Funding Distribution"

5. **City Performance Table**
   - Visual: Table
   - Columns:
     - `city`
     - `state`
     - `Total Startups`
     - `Total Deals`
     - `Total Funding (M)`
     - `Average Funding (M)`
   - Sort by Total Funding (desc)
   - Top 25 cities

6. **Geographic Trends Over Time**
   - Visual: Area Chart
   - X-axis: `year`
   - Y-axis: `Total Funding (B)`
   - Legend: `state` (Top 5 states only)
   - Stacked: Yes

#### Slicers:
- State multi-select
- City search box
- Industry filter

---

### PAGE 4: Investor & Clustering Insights

#### Layout Setup
1. Page title: "Investor Analysis & ML Clustering"
2. Background: White with accent border

#### Section A: Investor Analysis

1. **Top 20 Investors (Word Cloud or Bar)**
   - If using bar chart:
     - Parse investor names from `investors` column
     - Count occurrences
     - Show top 20
   - Alternative: Use Word Cloud custom visual from AppSource

2. **Investment Activity Timeline**
   - Visual: Line Chart
   - X-axis: `year_quarter`
   - Y-axis: `Total Deals`
   - Title: "Deal Flow Over Time"

3. **Funding Round Funnel**
   - Visual: Funnel Chart
   - Group: `funding_round`
   - Values: `Total Deals`
   - Order: Seed → Angel → Series A → Series B → etc.

4. **Round Type Performance**
   - Visual: Clustered Bar Chart
   - Y-axis: `funding_round`
   - Values: `Total Funding (M)` and `Average Funding (M)`
   - Legend: Measure names

#### Section B: Clustering Insights

5. **Cluster Distribution**
   - Visual: Donut Chart
   - Legend: `cluster_name` (from startup_clusters table)
   - Values: Count of startups
   - Title: "Startup Segments"
   - Data labels: Category and percentage

6. **Cluster Characteristics Table**
   - Visual: Matrix
   - Rows: `cluster_name`
   - Values:
     - Count of `startup_name`
     - Average `total_funding` (from cluster table)
     - Average `num_funding_rounds`
     - Sum `total_funding`

7. **Cluster Funding Comparison**
   - Visual: Clustered Column Chart
   - X-axis: `cluster_name`
   - Y-axis: Average total_funding (from clusters)
   - Data labels: On
   - Color: Gradient based on value

8. **Cluster Details Table**
   - Visual: Table
   - Columns (from startup_clusters):
     - `startup_name`
     - `cluster_name`
     - `total_funding` (formatted as millions)
     - `num_funding_rounds`
     - `industry_first`
   - Top 50 by total_funding

9. **Scatter Plot - Funding vs Rounds**
   - Visual: Scatter Chart
   - X-axis: `num_funding_rounds`
   - Y-axis: `total_funding`
   - Legend: `cluster_name`
   - Size: `total_funding`
   - Title: "Startup Clustering Pattern"

#### Slicers:
- Cluster name filter
- Industry filter
- Funding amount range

---

## 🎨 PART 4: Formatting & Design

### Color Theme
Use these colors consistently:

```
Primary Blue: #0078D4
Secondary Orange: #FF8C00
Success Green: #107C10
Accent Purple: #881798
Warning Red: #E81123
Neutral Gray: #767676
Background: #F5F5F5
White: #FFFFFF
```

### Typography
- **Headers**: Segoe UI, 16-20pt, Bold
- **Titles**: Segoe UI, 14pt, Semibold
- **Body**: Segoe UI, 11pt, Regular
- **Labels**: Segoe UI, 10pt

### General Formatting

1. **All visuals:**
   - Background: White
   - Border: 1px, light gray
   - Shadow: Subtle (optional)
   - Padding: 10px

2. **All titles:**
   - Font: Segoe UI
   - Size: 14pt
   - Color: Dark gray (#333333)
   - Background: Transparent

3. **Data labels:**
   - Font size: 9-10pt
   - Show only when space permits
   - Use abbreviated units (K, M, B)

4. **Tooltips:**
   - Enable for all charts
   - Add custom tooltip page with detailed info

---

## 🔄 PART 5: Interactivity & Filters

### Add Cross-filtering

1. Go to **Format** → **Edit interactions** for each visual
2. Set strategic interactions:
   - KPI cards: Don't filter
   - Year filter: Filters all visuals
   - Industry charts: Cross-filter other charts
   - Geographic visuals: Highlight related visuals

### Create Bookmarks

1. **Bookmark 1: Overview**
   - All filters cleared
   - Show overall metrics

2. **Bookmark 2: Top Sectors**
   - Filter to top 5 industries
   - Highlight sector page

3. **Bookmark 3: Recent Trends**
   - Filter to last 3 years
   - Focus on timeline charts

4. Add buttons to navigate between bookmarks

### Sync Slicers

1. View → Sync Slicers
2. Sync these across all pages:
   - Year slicer
   - Industry slicer
3. Make slicers consistent in position across pages

---

## 📊 PART 6: Advanced Features

### Custom Tooltips

1. Create new page: "Tooltip - Startup Details"
2. Set page size: Tooltip
3. Add visuals showing:
   - Startup name
   - Total funding
   - Number of rounds
   - Industries
   - Timeline chart

4. For main visuals, Format → Tooltip → Report page → Select custom tooltip page

### Drill-through Pages

1. Create "Startup Deep Dive" page
2. Add drill-through field: `startup_name`
3. Show detailed metrics for selected startup:
   - All funding rounds
   - Funding timeline
   - Investors involved
   - Industry comparison

### Mobile Layout

1. View → Mobile Layout
2. Rearrange visuals for mobile viewing
3. Prioritize:
   - KPI cards at top
   - Key charts in scrollable format
   - Simplify complex visuals

---

## 📤 PART 7: Publishing & Sharing

### Before Publishing

1. **Performance Optimization:**
   - Remove unused columns
   - Optimize DAX measures
   - Reduce visual complexity where possible

2. **Data Refresh:**
   - Set up scheduled refresh if using Power BI Service
   - Test manual refresh

3. **Final Checks:**
   - Test all filters
   - Verify all calculations
   - Check mobile view
   - Review tooltip functionality

### Publishing Steps

1. Click **File** → **Publish** → **Publish to Power BI**
2. Select workspace
3. After publishing:
   - Configure row-level security (if needed)
   - Set up scheduled refresh
   - Share with stakeholders

---

## 📋 Quick Reference: Key Visuals Summary

| Page | Visual Type | Purpose |
|------|-------------|---------|
| Overview | KPI Cards | Total funding, startups, deals, avg |
| Overview | Line + Column | Yearly trends |
| Overview | Bar Chart | Top industries |
| Overview | Donut | Funding rounds |
| Sector | Matrix | Industry metrics |
| Sector | Bar Charts | Sector rankings |
| Sector | Line Chart | Trends over time |
| Geographic | Map | State distribution |
| Geographic | Bar Charts | City rankings |
| Geographic | Treemap | Visual hierarchy |
| Investor | Funnel | Round progression |
| Investor | Scatter | Clustering patterns |
| Investor | Donut | Cluster distribution |

---

## 🎯 Expected Dashboard Look

### Overview Page Layout:
```
┌─────────────────────────────────────────────────────┐
│  INDIAN STARTUPS FUNDING ANALYSIS                   │
├────────┬────────┬────────┬────────┬────────────────┤
│ $XXB   │ X,XXX  │ X,XXX  │ $XXM   │ [Year Filter]  │
│ Total  │ Startups│ Deals │ Avg    │ [Industry]     │
├────────┴────────┴────────┴────────┴────────────────┤
│ ┌─────────────────────┐ ┌─────────────────────┐   │
│ │ Yearly Trend        │ │ Top Industries      │   │
│ │ (Line + Column)     │ │ (Bar Chart)         │   │
│ └─────────────────────┘ └─────────────────────┘   │
├──────────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Round Types  │ │ Top Cities   │ │ Growth KPI   │ │
│ │ (Donut)      │ │ (Treemap)    │ │ (Card)       │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
├──────────────────────────────────────────────────────┤
│ Top Deals Table                                      │
└──────────────────────────────────────────────────────┘
```

---

## ✅ Validation Checklist

Before finalizing:

- [ ] All data loaded correctly
- [ ] Relationships established
- [ ] All DAX measures working
- [ ] KPI cards showing correct values
- [ ] All charts rendering properly
- [ ] Filters working across pages
- [ ] Slicers synced appropriately
- [ ] Colors consistent with theme
- [ ] Titles and labels clear
- [ ] Mobile layout configured
- [ ] Tooltips functioning
- [ ] Drill-through working
- [ ] Performance acceptable (<5 sec load)
- [ ] All pages have titles
- [ ] Navigation intuitive

---

## 🆘 Troubleshooting

**Issue: Relationships not working**
- Solution: Check data types match, use startup_name as key field

**Issue: DAX measure errors**
- Solution: Ensure table names match exactly (check spelling)

**Issue: Visuals too slow**
- Solution: Reduce date granularity, limit to top N, use aggregations

**Issue: Map not showing locations**
- Solution: Ensure state names match Power BI geography exactly

**Issue: Cluster data not joining**
- Solution: Verify startup names match exactly between tables

---

## 📖 Additional Resources

For custom visuals:
- Visit [Microsoft AppSource](https://appsource.microsoft.com/marketplace/apps?product=power-bi-visuals)
- Recommended: Word Cloud, Enhanced Scatter, Drill Down Donut

For advanced DAX:
- [SQLBI DAX Guide](https://dax.guide)
- Power BI Community Forums

---

**Created by:** Data Science Team  
**Last Updated:** 2025-01-14  
**Dashboard Version:** 1.0
