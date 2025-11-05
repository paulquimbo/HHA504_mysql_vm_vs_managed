import os, time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import datetime

# --- 1) Load environment variables ---
load_dotenv(".env")  # Assumes .env is in current working directory

VM_DB_HOST = os.getenv("VM_DB_HOST")
VM_DB_PORT = os.getenv("VM_DB_PORT", "3306")
VM_DB_USER = os.getenv("VM_DB_USER")
VM_DB_PASS = os.getenv("VM_DB_PASS")
VM_DB_NAME = os.getenv("VM_DB_NAME")

print("[ENV] VM_DB_HOST:", VM_DB_HOST)
print("[ENV] VM_DB_PORT:", VM_DB_PORT)
print("[ENV] VM_DB_USER:", VM_DB_USER)
print("[ENV] VM_DB_NAME:", VM_DB_NAME)

# --- 2) Connect to server and ensure database exists ---
server_url = f"mysql+pymysql://{VM_DB_USER}:{VM_DB_PASS}@{VM_DB_HOST}:{VM_DB_PORT}"
print("[STEP 1] Connecting to MySQL server (no DB):", server_url.replace(VM_DB_PASS, "*****"))
t0 = time.time()

engine_server = create_engine(server_url, pool_pre_ping=True)
with engine_server.begin() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{VM_DB_NAME}`"))
    conn.commit()

print(f"[OK] Ensured database `{VM_DB_NAME}` exists. Time taken: {time.time() - t0:.2f}s")

# --- 3) Connect to the target database ---
db_url = f"mysql+pymysql://{VM_DB_USER}:{VM_DB_PASS}@{VM_DB_HOST}:{VM_DB_PORT}/{VM_DB_NAME}"
masked_url = db_url.replace(VM_DB_PASS, "*****")
print("[STEP 2] Connecting to DB:", masked_url)

engine = create_engine(db_url, pool_pre_ping=True)

# --- 4) Create a DataFrame and write to a table ---
table_name = "visits"
df = pd.DataFrame([
    {"patient_id": 1, "visit_date": "2025-09-01", "bp_sys": 118, "bp_dia": 76},
    {"patient_id": 2, "visit_date": "2025-09-02", "bp_sys": 130, "bp_dia": 85},
    {"patient_id": 3, "visit_date": "2025-09-03", "bp_sys": 121, "bp_dia": 79},
    {"patient_id": 4, "visit_date": "2025-09-04", "bp_sys": 110, "bp_dia": 70},
    {"patient_id": 5, "visit_date": "2025-09-05", "bp_sys": 125, "bp_dia": 82},
])

df.to_sql(table_name, con=engine, if_exists="replace", index=False)
print(f"[STEP 3] Wrote {len(df)} rows to `{table_name}` table.")

# --- 5) Read back a quick check ---
print("[STEP 4] Reading back row count ...")
with engine.connect() as conn:
    count_df = pd.read_sql(f"SELECT COUNT(*) AS n_rows FROM `{table_name}`", con=conn)
print(count_df)

elapsed = time.time() - t0
print(f"[DONE] VM path completed in {elapsed:.1f}s at {datetime.utcnow().isoformat()}Z")

