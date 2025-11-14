-- ============================================================
-- Indian Startups Funding Analysis - SQL Queries
-- Database: MySQL / PostgreSQL
-- Table: startup_funding
-- Author: Data Science Team
-- Date: 2025-01-14
-- ============================================================

-- ============================================================
-- 1. TOTAL FUNDING ANALYSIS
-- ============================================================

-- Total funding raised by all startups
SELECT 
    COUNT(*) AS total_funding_rounds,
    COUNT(DISTINCT startup_name) AS unique_startups,
    SUM(funding_amount_usd) AS total_funding_usd,
    AVG(funding_amount_usd) AS avg_funding_per_round,
    MIN(funding_amount_usd) AS min_funding,
    MAX(funding_amount_usd) AS max_funding
FROM startup_funding
WHERE funding_amount_usd > 0;

-- ============================================================
-- 2. YEAR-WISE FUNDING TREND
-- ============================================================

-- Yearly funding trends with growth metrics
SELECT 
    YEAR(date) AS funding_year,
    COUNT(*) AS num_deals,
    COUNT(DISTINCT startup_name) AS num_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_deal_size,
    MIN(funding_amount_usd) AS min_deal,
    MAX(funding_amount_usd) AS max_deal
FROM startup_funding
WHERE date IS NOT NULL
GROUP BY YEAR(date)
ORDER BY funding_year DESC;

-- Year-over-Year growth percentage
WITH yearly_funding AS (
    SELECT 
        YEAR(date) AS year,
        SUM(funding_amount_usd) AS total_funding
    FROM startup_funding
    WHERE date IS NOT NULL
    GROUP BY YEAR(date)
)
SELECT 
    year,
    total_funding,
    LAG(total_funding) OVER (ORDER BY year) AS prev_year_funding,
    ROUND(
        ((total_funding - LAG(total_funding) OVER (ORDER BY year)) / 
         LAG(total_funding) OVER (ORDER BY year) * 100), 2
    ) AS yoy_growth_pct
FROM yearly_funding
ORDER BY year DESC;

-- ============================================================
-- 3. TOP 10 SECTORS BY TOTAL FUNDING
-- ============================================================

SELECT 
    industry,
    COUNT(*) AS num_funding_rounds,
    COUNT(DISTINCT startup_name) AS num_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding_per_round,
    ROUND(SUM(funding_amount_usd) * 100.0 / (SELECT SUM(funding_amount_usd) FROM startup_funding), 2) AS pct_of_total_funding
FROM startup_funding
WHERE industry IS NOT NULL
GROUP BY industry
ORDER BY total_funding DESC
LIMIT 10;

-- ============================================================
-- 4. TOP 10 CITIES BY NUMBER OF FUNDED STARTUPS
-- ============================================================

SELECT 
    city,
    COUNT(DISTINCT startup_name) AS num_startups,
    COUNT(*) AS num_funding_rounds,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding
FROM startup_funding
WHERE city IS NOT NULL AND city != 'Unknown'
GROUP BY city
ORDER BY num_startups DESC
LIMIT 10;

-- ============================================================
-- 5. TOP 10 CITIES BY TOTAL FUNDING AMOUNT
-- ============================================================

SELECT 
    city,
    state,
    COUNT(DISTINCT startup_name) AS num_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding_per_round
FROM startup_funding
WHERE city IS NOT NULL AND city != 'Unknown'
GROUP BY city, state
ORDER BY total_funding DESC
LIMIT 10;

-- ============================================================
-- 6. MOST ACTIVE INVESTORS
-- ============================================================

-- Note: This query assumes investors are comma-separated in a single column
-- For normalized database, use JOIN with investors table

SELECT 
    investors,
    COUNT(*) AS num_investments,
    COUNT(DISTINCT startup_name) AS num_unique_startups,
    SUM(funding_amount_usd) AS total_funding_backed,
    AVG(funding_amount_usd) AS avg_investment_size
FROM startup_funding
WHERE investors IS NOT NULL 
    AND investors != 'Undisclosed'
    AND investors NOT LIKE '%,%'  -- Single investor deals
GROUP BY investors
ORDER BY num_investments DESC
LIMIT 20;

-- ============================================================
-- 7. AVERAGE FUNDING PER ROUND TYPE
-- ============================================================

SELECT 
    funding_round,
    COUNT(*) AS num_rounds,
    COUNT(DISTINCT startup_name) AS num_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding,
    MIN(funding_amount_usd) AS min_funding,
    MAX(funding_amount_usd) AS max_funding,
    STDDEV(funding_amount_usd) AS std_dev_funding
FROM startup_funding
WHERE funding_round IS NOT NULL AND funding_round != 'Unknown'
GROUP BY funding_round
ORDER BY avg_funding DESC;

-- ============================================================
-- 8. SECTOR-WISE SUMMARY STATISTICS
-- ============================================================

SELECT 
    industry,
    COUNT(*) AS total_rounds,
    COUNT(DISTINCT startup_name) AS unique_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding,
    MIN(funding_amount_usd) AS min_funding,
    MAX(funding_amount_usd) AS max_funding,
    STDDEV(funding_amount_usd) AS std_dev,
    -- Percentiles (using approximate method)
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY funding_amount_usd) AS percentile_25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY funding_amount_usd) AS median_funding,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY funding_amount_usd) AS percentile_75,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY funding_amount_usd) AS percentile_95
FROM startup_funding
WHERE industry IS NOT NULL
GROUP BY industry
HAVING COUNT(*) >= 10  -- Only sectors with at least 10 funding rounds
ORDER BY total_funding DESC;

-- ============================================================
-- 9. TOP FUNDED STARTUPS OF ALL TIME
-- ============================================================

SELECT 
    startup_name,
    industry,
    city,
    state,
    COUNT(*) AS num_funding_rounds,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_per_round,
    MIN(YEAR(date)) AS first_funding_year,
    MAX(YEAR(date)) AS latest_funding_year
FROM startup_funding
WHERE startup_name IS NOT NULL
GROUP BY startup_name, industry, city, state
ORDER BY total_funding DESC
LIMIT 25;

-- ============================================================
-- 10. MONTHLY FUNDING TRENDS (Last 24 Months)
-- ============================================================

SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month,
    COUNT(*) AS num_deals,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_deal_size
FROM startup_funding
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
GROUP BY DATE_FORMAT(date, '%Y-%m')
ORDER BY month DESC;

-- ============================================================
-- 11. FUNDING ROUND PROGRESSION FOR TOP STARTUPS
-- ============================================================

WITH top_startups AS (
    SELECT startup_name
    FROM startup_funding
    GROUP BY startup_name
    ORDER BY SUM(funding_amount_usd) DESC
    LIMIT 10
)
SELECT 
    sf.startup_name,
    sf.funding_round,
    sf.funding_amount_usd,
    sf.date,
    sf.investors
FROM startup_funding sf
INNER JOIN top_startups ts ON sf.startup_name = ts.startup_name
ORDER BY sf.startup_name, sf.date;

-- ============================================================
-- 12. INDUSTRY TRENDS BY YEAR
-- ============================================================

SELECT 
    industry,
    YEAR(date) AS year,
    COUNT(*) AS num_deals,
    SUM(funding_amount_usd) AS total_funding
FROM startup_funding
WHERE industry IS NOT NULL AND date IS NOT NULL
GROUP BY industry, YEAR(date)
ORDER BY industry, year DESC;

-- ============================================================
-- 13. STARTUP FUNDING VELOCITY (Deals per Quarter)
-- ============================================================

SELECT 
    YEAR(date) AS year,
    QUARTER(date) AS quarter,
    COUNT(*) AS num_deals,
    SUM(funding_amount_usd) AS total_funding,
    COUNT(DISTINCT startup_name) AS unique_startups,
    COUNT(DISTINCT industry) AS num_industries
FROM startup_funding
WHERE date IS NOT NULL
GROUP BY YEAR(date), QUARTER(date)
ORDER BY year DESC, quarter DESC;

-- ============================================================
-- 14. STARTUPS WITH MULTIPLE FUNDING ROUNDS
-- ============================================================

SELECT 
    startup_name,
    industry,
    city,
    COUNT(*) AS num_rounds,
    SUM(funding_amount_usd) AS total_funding,
    GROUP_CONCAT(DISTINCT funding_round ORDER BY date) AS funding_progression,
    DATEDIFF(MAX(date), MIN(date)) AS days_between_first_last
FROM startup_funding
WHERE startup_name IS NOT NULL
GROUP BY startup_name, industry, city
HAVING COUNT(*) > 1
ORDER BY num_rounds DESC, total_funding DESC
LIMIT 50;

-- ============================================================
-- 15. FUNDING CONCENTRATION ANALYSIS
-- ============================================================

-- Top 10% of startups vs. rest
WITH startup_totals AS (
    SELECT 
        startup_name,
        SUM(funding_amount_usd) AS total_funding
    FROM startup_funding
    GROUP BY startup_name
),
ranked_startups AS (
    SELECT 
        startup_name,
        total_funding,
        NTILE(10) OVER (ORDER BY total_funding DESC) AS decile
    FROM startup_totals
)
SELECT 
    decile,
    COUNT(*) AS num_startups,
    SUM(total_funding) AS total_funding,
    AVG(total_funding) AS avg_funding,
    ROUND(SUM(total_funding) * 100.0 / (SELECT SUM(total_funding) FROM ranked_startups), 2) AS pct_of_total
FROM ranked_startups
GROUP BY decile
ORDER BY decile;

-- ============================================================
-- END OF SQL QUERIES
-- ============================================================
