-- ==============================================================================
-- Astra AI — Snowflake Database, Tables, and Cortex Setup
-- Run this script in a Snowflake SQL Worksheet (Role: ACCOUNTADMIN or SYSADMIN)
-- ==============================================================================

-- 1. Setup Role, Warehouse, Database & Schema
USE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE IF NOT EXISTS ASTRA_WH
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

USE WAREHOUSE ASTRA_WH;

CREATE DATABASE IF NOT EXISTS ASTRA_AI_DB;
USE DATABASE ASTRA_AI_DB;

CREATE SCHEMA IF NOT EXISTS SURVEILLANCE;
USE SCHEMA SURVEILLANCE;

-- ------------------------------------------------------------------------------
-- 2. Create Surveillance Tables
-- ------------------------------------------------------------------------------

-- Customers Table
CREATE OR REPLACE TABLE CUSTOMERS (
    CUSTOMER_ID VARCHAR(50) PRIMARY KEY,
    FULL_NAME VARCHAR(255),
    COUNTRY VARCHAR(100),
    OCCUPATION VARCHAR(255),
    ACCOUNT_TYPE VARCHAR(50),
    KYC_STATUS VARCHAR(50),
    RISK_SCORE INT,
    RISK_LEVEL VARCHAR(20),
    IS_PEP BOOLEAN,
    MONTHLY_BASELINE_VOLUME FLOAT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Transactions Table
CREATE OR REPLACE TABLE TRANSACTIONS (
    TX_ID VARCHAR(50) PRIMARY KEY,
    CUSTOMER_ID VARCHAR(50),
    CUSTOMER_NAME VARCHAR(255),
    AMOUNT FLOAT,
    CURRENCY VARCHAR(10),
    TX_TYPE VARCHAR(50),
    COUNTERPARTY VARCHAR(255),
    ANOMALY_SCORE FLOAT,
    STATUS VARCHAR(50),
    TRIGGER_REASON VARCHAR(255),
    TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Regulatory Cases & SAR Workflows
CREATE OR REPLACE TABLE CASES (
    CASE_ID VARCHAR(50) PRIMARY KEY,
    CUSTOMER_ID VARCHAR(50),
    SUBJECT VARCHAR(255),
    ASSIGNED_TO VARCHAR(100),
    PRIORITY VARCHAR(20),
    STAGE VARCHAR(50),
    FILING_DEADLINE DATE,
    EVIDENCE_COUNT INT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ------------------------------------------------------------------------------
-- 3. Seed Realistic Institutional Compliance Data
-- ------------------------------------------------------------------------------

INSERT INTO CUSTOMERS (CUSTOMER_ID, FULL_NAME, COUNTRY, OCCUPATION, ACCOUNT_TYPE, KYC_STATUS, RISK_SCORE, RISK_LEVEL, IS_PEP, MONTHLY_BASELINE_VOLUME) VALUES
('CUST-1008', 'Vikramaditya Singhania', 'India', 'Import-Export Director', 'Corporate', 'Enhanced Due Diligence', 88, 'HIGH', TRUE, 480000.0),
('CUST-1003', 'Devendra Patil', 'India', 'Financial Broker', 'Savings', 'Verified', 78, 'HIGH', FALSE, 150000.0),
('CUST-1004', 'Hon. Rameshwar Prasad', 'India', 'Legislative Committee Member', 'Current', 'Enhanced Due Diligence', 82, 'HIGH', TRUE, 600000.0),
('CUST-1005', 'Global Trade Nexus LLC', 'United Arab Emirates', 'Cross-Border Commodities', 'Corporate', 'Verified', 68, 'MEDIUM', FALSE, 1500000.0),
('CUST-1009', 'Siddharth Verma', 'Singapore', 'Fintech Solutions Director', 'Current', 'Verified', 54, 'MEDIUM', FALSE, 320000.0),
('CUST-1001', 'Ananya Sharma', 'India', 'Lead Cloud Architect', 'Savings', 'Verified', 12, 'LOW', FALSE, 95000.0),
('CUST-1002', 'Rajesh Kumar Gupta', 'India', 'Wholesale Electronics Merchant', 'Current', 'Verified', 24, 'LOW', FALSE, 480000.0),
('CUST-1006', 'Dr. Priya Sundaram', 'United Kingdom', 'Chief Cardiologist', 'Savings', 'Verified', 15, 'LOW', FALSE, 180000.0),
('CUST-1007', 'Apex Logistics Corridors', 'Cyprus', 'Maritime Freight Transit', 'Corporate', 'Under Review', 74, 'HIGH', FALSE, 2800000.0),
('CUST-1010', 'Kavita Mehra', 'India', 'Architectural Designer', 'Savings', 'Verified', 18, 'LOW', FALSE, 140000.0);

INSERT INTO TRANSACTIONS (TX_ID, CUSTOMER_ID, CUSTOMER_NAME, AMOUNT, CURRENCY, TX_TYPE, COUNTERPARTY, ANOMALY_SCORE, STATUS, TRIGGER_REASON) VALUES
('TXN-88491', 'CUST-1008', 'Vikramaditya Singhania', 485000.0, 'INR', 'WIRE_OUTBOUND', 'Al-Bahrani General Trading (UAE)', 0.94, 'FLAGGED', 'Rapid Layering / High-Risk Corridor'),
('TXN-88489', 'CUST-1003', 'Devendra Patil', 99500.0, 'INR', 'CASH_DEPOSIT', 'Multiple Branch Cashiers', 0.88, 'FLAGGED', 'Smurfing / Structuring under reporting cap'),
('TXN-88485', 'CUST-1004', 'Hon. Rameshwar Prasad', 750000.0, 'INR', 'RTGS_INBOUND', 'Aethelgard Consulting S.A.', 0.91, 'UNDER_INVESTIGATION', 'PEP Exposure / Unexplained Wealth Order'),
('TXN-88480', 'CUST-1007', 'Apex Logistics Corridors', 1420000.0, 'USD', 'SWIFT_TRANSFER', 'Bosphorus Maritime Trading', 0.85, 'FLAGGED', 'Sanctions Proximity / Offshore Gateway'),
('TXN-88472', 'CUST-1005', 'Global Trade Nexus LLC', 320000.0, 'INR', 'VENDOR_PAYMENT', 'Shenzhen Electrotech Corp', 0.42, 'CLEARED', 'Standard Trade Flow'),
('TXN-88465', 'CUST-1001', 'Ananya Sharma', 18500.0, 'INR', 'UPI_TRANSFER', 'Urban Merchant Pay', 0.05, 'CLEARED', 'Normal Personal Spending'),
('TXN-88461', 'CUST-1009', 'Siddharth Verma', 125000.0, 'INR', 'NEFT_OUTBOUND', 'CloudScale Hosting SG', 0.38, 'CLEARED', 'Routine SaaS Billing');

INSERT INTO CASES (CASE_ID, CUSTOMER_ID, SUBJECT, ASSIGNED_TO, PRIORITY, STAGE, FILING_DEADLINE, EVIDENCE_COUNT) VALUES
('CASE-4091', 'CUST-1008', 'Singhania Trade Horizon Layering', 'Senior Risk Officer', 'CRITICAL', 'SAR In Preparation', '2026-10-08', 7),
('CASE-4088', 'CUST-1003', 'Structuring Inquiries — D. Patil Branches', 'Compliance Analyst', 'HIGH', 'Request for Information (RFI)', '2026-10-12', 4),
('CASE-4075', 'CUST-1007', 'Apex Logistics Bosphorus Sanctions Check', 'Chief Sanctions Officer', 'HIGH', 'Escalated to MLRO', '2026-10-09', 12);

-- ------------------------------------------------------------------------------
-- 4. Test Snowflake Cortex AI Integration
-- ------------------------------------------------------------------------------
-- Tests if Cortex is enabled in your account
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Summarize why transaction structuring and smurfing violates AML regulations in two concise bullet points.'
) AS CORTEX_REASONING_TEST;

-- ------------------------------------------------------------------------------
-- 5. (OPTIONAL) Snowpark Container Services (SPCS) Image Repository
-- Required only if deploying the full React + FastAPI Docker containers in Snowflake
-- ------------------------------------------------------------------------------
CREATE IMAGE REPOSITORY IF NOT EXISTS ASTRA_AI_DB.SURVEILLANCE.ASTRA_REPO;

SHOW IMAGE REPOSITORIES IN SCHEMA ASTRA_AI_DB.SURVEILLANCE;
