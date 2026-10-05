# Astra AI — Snowflake Console Deployment Guide

This guide walks you through deploying **Astra AI** inside your Snowflake Snowsight Console in under **2 minutes**.

---

## 🚀 Option 1: Native Streamlit in Snowflake (Recommended & Instant)

Deploy Astra AI directly inside your Snowflake console with **zero command-line or Docker setup**.

### Step 1: Open Streamlits in Snowflake
1. In your Snowflake Console (as seen on your Home screen):
   - Look at the top **Quick actions** or under **Recent projects**, click on the **Streamlits** tab.
   - Alternatively, click the **`+ New Project`** button and select **Streamlit** (or click **Projects > Streamlit** on the left navigation bar).

<p align="center">
  <em>(Click "+ New Project" -> "Streamlit" in your Snowflake Console)</em>
</p>

### Step 2: Configure the App
A creation dialog will appear:
- **App title**: `Astra AI - Risk & AML Surveillance`
- **App location**:
  - **Database**: Select any database (e.g. `DEMO_DB` or default)
  - **Schema**: `PUBLIC`
- **Warehouse**: Select your warehouse (e.g., `COMPUTE_WH`)
- Click **Create**.

### Step 3: Paste Astra AI Code
1. An in-browser Python editor will open with boilerplate sample code.
2. Select all code in that editor (`Ctrl + A`) and delete it.
3. Open the file [`snowflake_deployment/astra_ai_snowflake_app.py`](./astra_ai_snowflake_app.py) from this project.
4. Copy the entire file content and paste it into the Snowflake editor.
5. In the top right corner of the Snowflake editor, click **▶ Run**.

🎉 **That's it!** Astra AI is now live in your Snowflake Console with:
- Real-time AML/KYC Surveillance dashboards
- Flagged Transaction Stream with risk badges
- Interactive Neural Copilot (integrated with Snowflake Cortex AI)
- Case Management & SAR Workflows

---

## 🗄️ Option 2: Setup Native Snowflake Database & Tables (Optional)

If you would like Astra AI's compliance records stored natively in Snowflake relational tables:

1. In your Snowflake Console, click on **Projects > Worksheets** (or click **`+ New Project > SQL Worksheet`**).
2. Open [`snowflake_deployment/snowflake_setup.sql`](./snowflake_setup.sql).
3. Copy all SQL statements and paste them into the worksheet.
4. Click the blue **▶ Run All** button (top right).
5. This creates:
   - Database: `ASTRA_AI_DB`
   - Schema: `SURVEILLANCE`
   - Tables: `CUSTOMERS`, `TRANSACTIONS`, `CASES`
   - Cortex AI integration test!

---

## 🐳 Option 3: Snowpark Container Services (SPCS) (Full React + FastAPI)

For running the full multi-tier React SPA and FastAPI backend as a container inside Snowflake:

1. Run the image repository creation from `snowflake_setup.sql`:
   ```sql
   CREATE IMAGE REPOSITORY IF NOT EXISTS ASTRA_AI_DB.SURVEILLANCE.ASTRA_REPO;
   SHOW IMAGE REPOSITORIES IN SCHEMA ASTRA_AI_DB.SURVEILLANCE;
   ```
2. Copy the `repository_url` returned by `SHOW IMAGE REPOSITORIES`.
3. Build and push the Docker container to Snowflake:
   ```bash
   docker login <registry_url> -u <snowflake_user>
   docker build -t <registry_url>/astra_app:latest -f Dockerfile .
   docker push <registry_url>/astra_app:latest
   ```
4. Create the container service in a SQL worksheet:
   ```sql
   CREATE COMPUTE POOL ASTRA_COMPUTE_POOL
       MIN_NODES = 1 MAX_NODES = 1
       INSTANCE_FAMILY = CPU_X64_XS;

   CREATE SERVICE ASTRA_AI_DB.SURVEILLANCE.ASTRA_WEB_SERVICE
       IN COMPUTE POOL ASTRA_COMPUTE_POOL
       FROM SPECIFICATION @ASTRA_STAGE/astra_spec.yaml;
   ```
