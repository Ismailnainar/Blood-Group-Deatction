import pyodbc
import sys

database = 'Bloodgroup'
username = 'blood'
password = 'Blood@123'
driver = '{ODBC Driver 17 for SQL Server}'

def test_connection(server_addr, desc):
    print(f"Testing connection to {desc} ({server_addr})...")
    conn_str = f'DRIVER={driver};SERVER={server_addr};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    try:
        cnxn = pyodbc.connect(conn_str, timeout=5)
        print(f"SUCCESS: Connected to {desc}")
        cnxn.close()
    except Exception as e:
        print(f"FAILURE: Could not connect to {desc}: {e}")

test_connection('192.168.1.8', 'LAN IP')
print("-" * 20)
test_connection('127.0.0.1', 'Localhost IP')
print("-" * 20)
test_connection('localhost', 'Localhost Hostname')
