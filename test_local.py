import pyodbc
import sys

database = 'Bloodgroup'
username = 'blood'
password = 'Blood@123'
driver = '{ODBC Driver 17 for SQL Server}'
server_local = '127.0.0.1'

print(f"Testing connection to {server_local}...")
try:
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server_local+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password, timeout=5)
    print("SUCCESS: Connected to 127.0.0.1")
    cnxn.close()
except Exception as e:
    print(f"FAILURE: Could not connect to 127.0.0.1: {e}")
