<h1 align="center">📊 Medallion Architecture — JIRA SLA Data Pipeline</h1>

<p align="center">
Python Data Engineering project implementing a Medallion Architecture (Bronze → Silver → Gold)
</p>

<hr>

<h2>🧠 Project Overview</h2>

<p>
This project implements a <strong>Data Engineering pipeline in Python</strong> following the
<strong>Medallion Architecture</strong> pattern.
</p>

<p>The pipeline:</p>
<ul>
  <li>Ingests JIRA issue data from Azure Blob Storage</li>
  <li>Processes nested JSON structures</li>
  <li>Calculates SLA metrics based on business rules</li>
  <li>Generates aggregated analytical reports</li>
</ul>

<hr>

<h2>🏗️ Architecture Layers</h2>

<h3>🥉 Bronze — Raw Ingestion</h3>
<ul>
  <li>Reads JSON from Azure Blob Storage</li>
  <li>Stores raw file locally</li>
  <li>No transformation applied</li>
</ul>

<p><strong>Output:</strong></p>
<pre>data/bronze/bronze_issues.json</pre>

<hr>

<h3>🥈 Silver — Clean & Structured Data</h3>
<ul>
  <li>Flatten nested JSON</li>
  <li>Extract relevant fields</li>
  <li>Standardize column names</li>
  <li>Convert dates to UTC</li>
  <li>Remove invalid date records</li>
  <li>Keep all statuses (including Open)</li>
</ul>

<p><strong>Output:</strong></p>
<pre>data/silver/silver_issues.parquet</pre>

<hr>

<h3>🥇 Gold — Business Logic & Reporting</h3>
<ul>
  <li>Filter only Done and Resolved issues</li>
  <li>Calculate SLA resolution time (business hours)</li>
  <li>Exclude weekends</li>
  <li>Exclude national holidays (via public API)</li>
  <li>Generate final SLA table</li>
  <li>Generate aggregated reports</li>
</ul>

<p><strong>Outputs:</strong></p>
<pre>
data/gold/gold_sla_issues.csv
data/gold/gold_sla_by_analyst.csv
data/gold/gold_sla_by_issue_type.csv
</pre>

<hr>

<h2>🧩 SLA Business Rules</h2>

<table border="1" cellpadding="6">
<tr>
<th>Priority</th>
<th>Expected SLA</th>
</tr>
<tr>
<td>High</td>
<td>24 hours</td>
</tr>
<tr>
<td>Medium</td>
<td>72 hours</td>
</tr>
<tr>
<td>Low</td>
<td>120 hours</td>
</tr>
</table>

<p>SLA calculation considers:</p>
<ul>
  <li>Business hours only</li>
  <li>Exclusion of weekends</li>
  <li>Exclusion of national holidays</li>
  <li>Partial first and last day calculation</li>
</ul>

<hr>

<h2>🧠 SLA Logic Implementation</h2>

<p>The SLA logic is implemented in:</p>
<pre>src/sla_calculation.py</pre>

<p>Main functions:</p>
<ul>
  <li><code>get_sla_expected_hours(priority)</code></li>
  <li><code>get_national_holidays(year)</code></li>
  <li><code>calculate_business_hours(start, end, holidays)</code></li>
  <li><code>check_sla_compliance(resolution_hours, expected_sla)</code></li>
</ul>

<hr>

<h2>📂 Project Structure</h2>

<pre>
Medallion-Architecture/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── sla_calculation.py
│
├── requirements.txt
├── README.md
└── .gitignore
</pre>

<hr>

<h2>⚙️ Environment Setup</h2>

<h3>1️⃣ Create Virtual Environment</h3>

<pre>
python -m venv .venv
</pre>

<p><strong>Activate:</strong></p>

<pre>
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
</pre>

<h3>2️⃣ Install Dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<hr>

<h2>🔐 Environment Variables</h2>

<p>Create a <code>.env</code> file in the project root:</p>

<pre>
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
ACCOUNT_URL=
CONTAINER_NAME=
BLOB_NAME=
</pre>

<p>These credentials authenticate Azure Blob access using Service Principal.</p>

<hr>

<h2>📦 Dependencies</h2>

<pre>
azure-identity==1.17.1
azure-storage-blob==12.19.1
python-dotenv==1.0.1
pandas==2.2.2
pyarrow==15.0.2
requests==2.32.3
</pre>

<hr>

<h2>📊 Data Dictionary — Gold Output</h2>

<table border="1" cellpadding="6">
<tr>
<th>Column</th>
<th>Description</th>
</tr>
<tr>
<td>issue_id</td>
<td>Unique ticket identifier</td>
</tr>
<tr>
<td>issue_type</td>
<td>Type of issue</td>
</tr>
<tr>
<td>assignee_name</td>
<td>Responsible analyst</td>
</tr>
<tr>
<td>priority</td>
<td>Ticket priority</td>
</tr>
<tr>
<td>created_at</td>
<td>Creation timestamp</td>
</tr>
<tr>
<td>resolved_at</td>
<td>Resolution timestamp</td>
</tr>
<tr>
<td>resolution_hours</td>
<td>Business hours to resolve</td>
</tr>
<tr>
<td>sla_expected_hours</td>
<td>SLA target based on priority</td>
</tr>
<tr>
<td>is_sla_met</td>
<td>SLA compliance indicator</td>
</tr>
</table>

<hr>

<h2>📈 Generated Reports</h2>

<ul>
  <li><strong>SLA by Analyst</strong>
    <ul>
      <li>Analyst name</li>
      <li>Number of issues</li>
      <li>Average SLA (business hours)</li>
    </ul>
  </li>
  <li><strong>SLA by Issue Type</strong>
    <ul>
      <li>Issue type</li>
      <li>Number of issues</li>
      <li>Average SLA (business hours)</li>
    </ul>
  </li>
</ul>

<hr>

<h2>🎯 Design Decisions</h2>

<ul>
  <li>Parquet used in Silver layer for performance and schema consistency</li>
  <li>CSV used in Gold layer for business-friendly reporting</li>
  <li>Modular SLA logic for maintainability</li>
  <li>Minimal and essential dependencies</li>
  <li>Clear separation of concerns across pipeline layers</li>
</ul>

<hr>

<h2>🚀 Running the Full Pipeline</h2>

<pre>
python src/bronze/ingest_bronze.py
python src/silver/transform_silver.py
python src/gold/build_gold.py
</pre>

<hr>

<h2>👩‍💻 Author</h2>

<p>
<strong>Lívia Marques Rodrigues</strong><br>
</p>
