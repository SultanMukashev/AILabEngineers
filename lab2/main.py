import psycopg2
import csv
from pathlib import Path
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env-non-dev
env_path = Path(__file__).parent.parent / '.env-non-dev'
load_dotenv(env_path)

# Database connection parameters
DB_PARAMS = {
    'dbname': os.getenv('POSTGRES_DB', 'postgres_beket'),
    'user': os.getenv('POSTGRES_USER', 'beket'),
    'password': os.getenv('POSTGRES_PASSWORD', 'beket'),
    'host': os.getenv('POSTGRES_HOST', 'postgres_db'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

print("Connecting with parameters:", {k: v if k != 'password' else '****' for k, v in DB_PARAMS.items()})

# SQL DDL statements
CREATE_TABLES = """
-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address_1 VARCHAR(100) NOT NULL,
    address_2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    join_date DATE NOT NULL
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_code VARCHAR(10) NOT NULL,
    product_description VARCHAR(100) NOT NULL
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(100) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    product_code VARCHAR(10) NOT NULL,
    product_description VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    account_id INTEGER NOT NULL REFERENCES accounts(customer_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_accounts_join_date ON accounts(join_date);
CREATE INDEX IF NOT EXISTS idx_products_code ON products(product_code);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_product ON transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id);
"""

def connect_to_db(max_retries=5, retry_delay=2):
    """Establish database connection with retries"""
    retries = 0
    last_exception = None
    
    while retries < max_retries:
        try:
            print(f"Attempting to connect to database (attempt {retries + 1}/{max_retries})...")
            conn = psycopg2.connect(**DB_PARAMS)
            print("Successfully connected to database!")
            return conn
        except Exception as e:
            last_exception = e
            print(f"Connection attempt {retries + 1} failed: {str(e)}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    print(f"Failed to connect after {max_retries} attempts")
    raise last_exception

def cleanup_tables(conn):
    """Clean up existing data from tables in correct order"""
    try:
        with conn.cursor() as cur:
            print("Cleaning up existing data...")
            # Delete in reverse order of dependencies
            cur.execute("TRUNCATE TABLE transactions, products, accounts CASCADE;")
        conn.commit()
        print("Successfully cleaned up tables!")
    except Exception as e:
        print(f"Error cleaning up tables: {str(e)}")
        conn.rollback()
        raise

def create_tables(conn):
    """Create database tables"""
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLES)
        conn.commit()
        print("Successfully created tables and indexes!")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        conn.rollback()
        raise

def clean_csv_value(value):
    """Clean CSV value by removing whitespace and handling empty strings"""
    if value is None:
        return None
    value = value.strip()
    return value if value else None

def parse_date(date_str):
    """Parse date string from CSV"""
    if not date_str:
        return None
    date_str = date_str.strip()
    try:
        # Assuming date format is YYYY/MM/DD
        year, month, day = map(int, date_str.split('/'))
        return f"{year:04d}-{month:02d}-{day:02d}"
    except:
        return None

def import_csv_data(conn, file_path, table_name):
    """Import data from CSV file into specified table"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read the header line and clean column names
            header = f.readline().strip()
            columns = [col.strip() for col in header.split(',')]
            
            # Create CSV reader with the cleaned header
            f.seek(0)  # Go back to start of file
            reader = csv.DictReader(f, fieldnames=columns, skipinitialspace=True)
            next(reader)  # Skip header row
            
            # Prepare INSERT statement
            placeholders = ','.join(['%s'] * len(columns))
            insert_query = f"""
                INSERT INTO {table_name} ({','.join(columns)})
                VALUES ({placeholders})
            """
            
            # Insert data
            with conn.cursor() as cur:
                for row in reader:
                    # Clean and prepare values
                    values = []
                    for col in columns:
                        value = clean_csv_value(row[col])
                        # Special handling for date fields
                        if col in ['join_date', 'transaction_date'] and value:
                            value = parse_date(value)
                        # Special handling for numeric fields
                        elif col in ['customer_id', 'product_id', 'quantity']:
                            value = int(value) if value else None
                        values.append(value)
                    
                    try:
                        cur.execute(insert_query, values)
                    except Exception as e:
                        print(f"Error inserting row: {row}")
                        print(f"Values: {values}")
                        raise
                
        conn.commit()
        print(f"Successfully imported data from {file_path}")
    except Exception as e:
        print(f"Error importing data from {file_path}: {str(e)}")
        conn.rollback()
        raise

def main():
    """Main function to orchestrate the data import process"""
    try:
        # Connect to database
        conn = connect_to_db()
        
        # Create tables
        create_tables(conn)
        
        # Clean up existing data
        cleanup_tables(conn)
        
        # Define data directory and CSV files in order of dependency
        data_dir = Path('data')
        csv_files = [
            ('accounts.csv', 'accounts'),
            ('products.csv', 'products'),
            ('transactions.csv', 'transactions')
        ]
        
        # Import data from each CSV file in the correct order
        for csv_file, table_name in csv_files:
            file_path = data_dir / csv_file
            print(f"\nImporting {csv_file} into {table_name} table...")
            import_csv_data(conn, file_path, table_name)
        
        print("\nData import completed successfully!")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()