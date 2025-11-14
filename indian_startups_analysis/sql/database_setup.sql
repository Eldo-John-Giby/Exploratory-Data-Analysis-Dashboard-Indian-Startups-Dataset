-- ============================================================
-- Database Setup Script for Indian Startups Funding Analysis
-- Database: MySQL / PostgreSQL
-- Author: Data Science Team
-- Date: 2025-01-14
-- ============================================================

-- Create database
CREATE DATABASE IF NOT EXISTS indian_startups_db;
USE indian_startups_db;

-- ============================================================
-- Create startup_funding table
-- ============================================================

CREATE TABLE IF NOT EXISTS startup_funding (
    id INT AUTO_INCREMENT PRIMARY KEY,
    startup_name VARCHAR(255) NOT NULL,
    industry VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    funding_amount_usd DECIMAL(18, 2),
    funding_round VARCHAR(100),
    investors TEXT,
    date DATE,
    year INT,
    month INT,
    quarter INT,
    month_name VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_startup_name (startup_name),
    INDEX idx_industry (industry),
    INDEX idx_city (city),
    INDEX idx_state (state),
    INDEX idx_year (year),
    INDEX idx_date (date),
    INDEX idx_funding_round (funding_round)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Load data from CSV
-- ============================================================

-- Note: Update the file path to match your system
-- For MySQL:
LOAD DATA INFILE '/path/to/cleaned_startup_data.csv'
INTO TABLE startup_funding
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(startup_name, industry, city, state, funding_amount_usd, funding_round, investors, date, year, month, quarter, month_name);

-- For PostgreSQL:
-- COPY startup_funding(startup_name, industry, city, state, funding_amount_usd, funding_round, investors, date, year, month, quarter, month_name)
-- FROM '/path/to/cleaned_startup_data.csv'
-- DELIMITER ','
-- CSV HEADER;

-- ============================================================
-- Create additional tables for normalized structure (Optional)
-- ============================================================

-- Industries table
CREATE TABLE IF NOT EXISTS industries (
    industry_id INT AUTO_INCREMENT PRIMARY KEY,
    industry_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Locations table
CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    UNIQUE KEY unique_location (city, state),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Investors table (for normalized structure)
CREATE TABLE IF NOT EXISTS investors (
    investor_id INT AUTO_INCREMENT PRIMARY KEY,
    investor_name VARCHAR(255) UNIQUE NOT NULL,
    investor_type VARCHAR(100), -- VC, Angel, PE, etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Funding rounds table (normalized)
CREATE TABLE IF NOT EXISTS funding_rounds (
    round_id INT AUTO_INCREMENT PRIMARY KEY,
    round_name VARCHAR(100) UNIQUE NOT NULL,
    round_order INT, -- Seed=1, Series A=2, etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Insert common funding rounds
INSERT INTO funding_rounds (round_name, round_order) VALUES
('Seed', 1),
('Angel', 2),
('Pre-Series A', 3),
('Series A', 4),
('Series B', 5),
('Series C', 6),
('Series D', 7),
('Series E', 8),
('Series F', 9),
('Bridge Round', 10),
('Debt Financing', 11),
('Private Equity', 12),
('IPO', 13),
('Unknown', 99)
ON DUPLICATE KEY UPDATE round_name = round_name;

-- ============================================================
-- Create views for common queries
-- ============================================================

-- View: Yearly funding summary
CREATE OR REPLACE VIEW v_yearly_funding_summary AS
SELECT 
    year,
    COUNT(*) AS total_deals,
    COUNT(DISTINCT startup_name) AS unique_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_deal_size,
    MIN(funding_amount_usd) AS min_funding,
    MAX(funding_amount_usd) AS max_funding
FROM startup_funding
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year DESC;

-- View: Industry performance
CREATE OR REPLACE VIEW v_industry_performance AS
SELECT 
    industry,
    COUNT(*) AS num_deals,
    COUNT(DISTINCT startup_name) AS num_startups,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding,
    MAX(funding_amount_usd) AS max_funding
FROM startup_funding
WHERE industry IS NOT NULL
GROUP BY industry
ORDER BY total_funding DESC;

-- View: Geographic distribution
CREATE OR REPLACE VIEW v_geographic_distribution AS
SELECT 
    state,
    city,
    COUNT(DISTINCT startup_name) AS num_startups,
    COUNT(*) AS num_deals,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_funding
FROM startup_funding
WHERE city IS NOT NULL AND state IS NOT NULL
GROUP BY state, city
ORDER BY total_funding DESC;

-- View: Top funded startups
CREATE OR REPLACE VIEW v_top_funded_startups AS
SELECT 
    startup_name,
    industry,
    city,
    state,
    COUNT(*) AS num_rounds,
    SUM(funding_amount_usd) AS total_funding,
    AVG(funding_amount_usd) AS avg_per_round,
    MIN(year) AS first_funding_year,
    MAX(year) AS latest_funding_year,
    MAX(year) - MIN(year) + 1 AS years_active
FROM startup_funding
WHERE startup_name IS NOT NULL
GROUP BY startup_name, industry, city, state
ORDER BY total_funding DESC;

-- ============================================================
-- Create stored procedures
-- ============================================================

DELIMITER //

-- Procedure: Get startup funding history
CREATE PROCEDURE IF NOT EXISTS sp_get_startup_history(IN p_startup_name VARCHAR(255))
BEGIN
    SELECT 
        date,
        funding_round,
        funding_amount_usd,
        investors,
        year
    FROM startup_funding
    WHERE startup_name = p_startup_name
    ORDER BY date;
END //

-- Procedure: Get industry trends by year
CREATE PROCEDURE IF NOT EXISTS sp_industry_trends(IN p_industry VARCHAR(255))
BEGIN
    SELECT 
        year,
        COUNT(*) AS num_deals,
        SUM(funding_amount_usd) AS total_funding,
        AVG(funding_amount_usd) AS avg_funding
    FROM startup_funding
    WHERE industry = p_industry
    GROUP BY year
    ORDER BY year DESC;
END //

-- Procedure: Get top performers in a city
CREATE PROCEDURE IF NOT EXISTS sp_top_startups_by_city(IN p_city VARCHAR(100), IN p_limit INT)
BEGIN
    SELECT 
        startup_name,
        industry,
        SUM(funding_amount_usd) AS total_funding,
        COUNT(*) AS num_rounds
    FROM startup_funding
    WHERE city = p_city
    GROUP BY startup_name, industry
    ORDER BY total_funding DESC
    LIMIT p_limit;
END //

DELIMITER ;

-- ============================================================
-- Create indexes for performance optimization
-- ============================================================

CREATE INDEX idx_funding_amount ON startup_funding(funding_amount_usd);
CREATE INDEX idx_startup_industry ON startup_funding(startup_name, industry);
CREATE INDEX idx_city_state ON startup_funding(city, state);
CREATE INDEX idx_year_industry ON startup_funding(year, industry);
CREATE INDEX idx_composite_analysis ON startup_funding(year, industry, city);

-- ============================================================
-- Grant permissions (update username as needed)
-- ============================================================

-- GRANT SELECT, INSERT, UPDATE ON indian_startups_db.* TO 'analyst_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ============================================================
-- Verification queries
-- ============================================================

-- Check row count
SELECT COUNT(*) AS total_records FROM startup_funding;

-- Check data completeness
SELECT 
    COUNT(*) AS total_rows,
    COUNT(startup_name) AS has_startup_name,
    COUNT(industry) AS has_industry,
    COUNT(funding_amount_usd) AS has_funding_amount,
    COUNT(date) AS has_date
FROM startup_funding;

-- Check date range
SELECT 
    MIN(date) AS earliest_date,
    MAX(date) AS latest_date,
    MIN(year) AS earliest_year,
    MAX(year) AS latest_year
FROM startup_funding;

-- ============================================================
-- END OF SETUP SCRIPT
-- ============================================================

SELECT 'Database setup completed successfully!' AS status;
