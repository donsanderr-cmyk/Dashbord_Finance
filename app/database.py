import sqlite3
import os
import pandas as pd

# =====================
# DB PATH SETUP
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


# =====================
# CREATE TABLE
# =====================
def create_table():

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,

            income REAL,
            expense REAL,
            assets REAL,
            liabilities REAL,
            savings REAL

        )
        """)

        conn.commit()


# =====================
# INSERT SINGLE DATA
# =====================
def insert_data(name, income, expense, assets, liabilities, savings):

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO financial_data (
            name,
            income,
            expense,
            assets,
            liabilities,
            savings
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name.strip(),
            float(income),
            float(expense),
            float(assets),
            float(liabilities),
            float(savings)
        ))

        conn.commit()


# =====================
# GET ALL DATA
# =====================
def get_all_data():

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM financial_data")
        rows = cursor.fetchall()

    return rows


# =====================
# INSERT DATAFRAME (UPLOAD EXCEL SAFE)
# =====================
def insert_dataframe(df: pd.DataFrame):

    df = df.copy()

    # normalize column names
    df.columns = df.columns.str.lower().str.strip()

    required_columns = [
        "name",
        "income",
        "expense",
        "assets",
        "liabilities",
        "savings"
    ]

    # validate columns
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # filter + clean
    df = df[required_columns]
    df = df.fillna(0)

    # convert numeric safely
    for col in required_columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            "financial_data",
            conn,
            if_exists="append",
            index=False
        )

def delete_all_data():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM financial_data")

    conn.commit()
    conn.close()